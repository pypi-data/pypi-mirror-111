import numpy as np
from hyperopt import Trials, STATUS_OK, STATUS_FAIL
import hyperopt
from sklearn import metrics
import pandas as pd
import pickle
import math
from sklearn.metrics import accuracy_score
from inspect import getfullargspec
from aironsuit.utils import load_model, save_model, clear_session
from aironsuit.trainers import *

BACKEND = get_backend()


class AIronSuit(object):
    """AIronSuit is a model wrapper that takes care of the hyper-parameter optimization problem, training and inference
    among other things.

    :param model_constructor: A model constructor function.
    :type model_constructor: function:`airontools.net_constructors.net_constructor`
    :param trainer: A class that trains the model constructed by model_constructor.
    :type trainer: class:`aironsuit.trainers.AIronTrainer`
    :param model_constructor_wrapper: A function that wraps the output model of the model_constructor.
    :type model_constructor_wrapper: function, optional
    """

    def __init__(self, model_constructor, trainer=None, model_constructor_wrapper=None):

        self.__model = None
        self.__trainer = None
        self.__model_constructor = model_constructor
        self.__trainer_class = AIronTrainer if not trainer else trainer
        self.__model_constructor_wrapper = model_constructor_wrapper
        self.__cuda = None
        self.__devices = None
        self.__total_n_models = None

    def create(self, specs, n_parallel_models=1, devices=None, cuda=None):
        """

        :param specs:
        :param n_parallel_models:
        :param devices:
        :param cuda:
        """
        self.__cuda = cuda
        self.__devices = devices if devices else []
        self.__total_n_models = n_parallel_models * len(self.__devices)
        self.__model = self.__model_constructor(**specs)
        if self.__model_constructor_wrapper:
            self.__model_constructor_wrapper(self.__model)
        if self.__cuda in specs and BACKEND != 'tensorflow':
            self.__model.cuda()

    def explore(self, x_train, y_train, x_val, y_val, space, model_specs, train_specs, path, max_evals, epochs,
                metric=None, trials=None, net_name='NN', verbose=0, seed=None, val_inference_in_path=None,
                callbacks=None, cuda=None):
        """

        :param x_train:
        :param y_train:
        :param x_val:
        :param y_val:
        :param space:
        :param model_specs:
        :param train_specs:
        :param path:
        :param max_evals:
        :param epochs:
        :param metric:
        :param trials:
        :param net_name:
        :param verbose:
        :param seed:
        :param val_inference_in_path:
        :param callbacks:
        :param cuda:
        :return:
        """
        self.__cuda = cuda
        if trials is None:
            trials = Trials()

        def objective(space):

            # Create model
            specs = space.copy()
            specs.update(model_specs)
            model = self.__model_constructor(**specs)
            if self.__model_constructor_wrapper:
                self.__model_constructor_wrapper(model)
            if self.__cuda in specs and BACKEND != 'tensorflow':
                model.cuda()

            # Print some information
            iteration = len(trials.losses())
            if verbose > 0:
                print('\n')
                print('iteration : {}'.format(0 if trials.losses() is None else iteration))
                [print('{}: {}'.format(key, value)) for key, value in specs.items()]
                print(model.summary(line_length=200))

            # Train model
            trainer_kargs = train_specs.copy()
            trainer_kargs.update({'module': model})
            if callbacks:
                trainer_kargs.update({'callbacks': callbacks})
            trainer = self.__trainer_class(**trainer_kargs)
            train_kargs = {}
            if not any([val_ is None for val_ in [x_val, y_val]]) and \
                    all([val_ in list(getfullargspec(trainer.fit))[0] for val_ in ['x_val', 'y_val']]):
                train_kargs.update({'x_val': x_train, 'y_val': y_train})
            train_kargs.update({'epochs': epochs})
            for karg, val in zip(['verbose'], [verbose]):
                if karg in list(getfullargspec(trainer.fit))[0]:
                    train_kargs.update({'verbose': val})
            trainer.fit(x_train, y_train, **train_kargs)

            # Exploration loss
            exp_loss = None  # ToDo: compatible with custom metric
            if metric in [None, 'categorical_accuracy', 'accuracy']:
                def prepare_for_acc(x):
                    if not isinstance(x, list):
                        x_ = [x]
                    else:
                        x_ = x.copy()
                    for i in range(len(x_)):
                        if len(x_[i].shape) == 1:
                            x_[i] = np.where(x_[i] > 0.5, 1, 0)
                        else:
                            x_[i] = np.argmax(x_[i], axis=-1)
                    return x_
                y_pred = prepare_for_acc(trainer.predict(x_val))
                y_val_ = prepare_for_acc(y_val)
                acc_score = []
                for i in range(len(y_pred)):
                    acc_score.append(accuracy_score(y_pred[i],  y_val_[i]))
                exp_loss = 1 - np.mean(acc_score)
            elif metric == 'i_auc':  # ToDo: make this work
                y_pred = model.predict(x_val)
                if not isinstance(y_pred, list):
                    y_pred = [y_pred]
                exp_loss = []
                for i in np.arange(0, self.__total_n_models):
                    if len(np.bincount(y_val[i][:, -1])) > 1 and not math.isnan(np.sum(y_pred[i])):
                        fpr, tpr, thresholds = metrics.roc_curve(y_val[i][:, -1], y_pred[i][:, -1])
                        exp_loss += [(1 - metrics.auc(fpr, tpr))]
                exp_loss = np.mean(exp_loss) if len(exp_loss) > 0 else 1
            if verbose > 0:
                print('\n')
                print('Exploration Loss: ', exp_loss)
            status = STATUS_OK if not math.isnan(exp_loss) and exp_loss is not None else STATUS_FAIL

            # Save trials
            with open(path + 'trials.hyperopt', 'wb') as f:
                pickle.dump(trials, f)

            # Save model if it is the best so far
            best_exp_losss_name = path + 'best_' + net_name + '_exp_loss'
            trials_losses = [loss_ for loss_ in trials.losses() if loss_]
            best_exp_loss = min(trials_losses) if len(trials_losses) > 0 else None
            print('best val loss so far: ', best_exp_loss)
            print('current val loss: ', exp_loss)
            best_exp_loss_cond = best_exp_loss is None or exp_loss < best_exp_loss
            print('save: ', status, best_exp_loss_cond)
            if status == STATUS_OK and best_exp_loss_cond:
                df = pd.DataFrame(data=[exp_loss], columns=['best_exp_loss'])
                df.to_pickle(best_exp_losss_name)
                self.__save_model(model=model, name=path + 'best_exp_' + net_name + '_json')
                with open(path + 'best_exp_' + net_name + '_hparams', 'wb') as f:
                    pickle.dump(space, f, protocol=pickle.HIGHEST_PROTOCOL)
                if val_inference_in_path is not None:
                    y_val_ = np.concatenate(y_val, axis=1) if isinstance(y_val, list) else y_val
                    np.savetxt(val_inference_in_path + 'val_target.csv', y_val_, delimiter=',')
                    y_inf = trainer.predict(x_val)
                    y_inf = np.concatenate(y_inf, axis=1) if isinstance(y_inf, list) else y_inf
                    np.savetxt(val_inference_in_path + 'val_target_inference.csv', y_inf, delimiter=',')

            clear_session()
            del model

            return {'loss': exp_loss, 'status': status}

        def optimize():

            if len(trials.trials) < max_evals:
                hyperopt.fmin(
                    objective,
                    rstate=None if seed is None else np.random.RandomState(seed),
                    space=space,
                    algo=hyperopt.tpe.suggest,
                    max_evals=max_evals,
                    trials=trials,
                    verbose=True,
                    return_argmin=False)
            with open(path + 'best_exp_' + net_name + '_hparams', 'rb') as f:
                best_hparams = pickle.load(f)

            # Best model
            specs = model_specs.copy()
            specs.update(best_hparams)
            best_model = self.__load_model(name=path + 'best_exp_' + net_name + '_json')
            if BACKEND == 'tensorflow':
                best_model.compile(optimizer=specs['optimizer'], loss=specs['loss'])
            else:
                best_model.cuda()
            print('best hyperparameters: ' + str(best_hparams))

            # Trainer
            trainer_kargs = train_specs.copy()
            trainer_kargs.update({'module': best_model})
            if callbacks:
                trainer_kargs.update({'callbacks': callbacks})
            trainer = self.__trainer_class(**trainer_kargs)
            if hasattr(trainer, 'initialize') and callable(trainer.initialize):
                trainer.initialize()

            return best_model, trainer

        self.__model, self.__trainer = optimize()

    def inference(self, x, use_trainer=False):
        """

        :param x:
        :return:
        """
        if use_trainer:
            if self.__trainer:
                inf_instance = self.__trainer
            else:
                inf_instance = self.__trainer_class(module=self.__model)
                if hasattr(inf_instance, 'initialize') and callable(inf_instance.initialize):
                    inf_instance.initialize()
        else:
            inf_instance = self.__model
        return inf_instance.predict(x)

    def save_model(self, name):
        """

        :param name:
        """
        self.__save_model(model=self.__model, name=name)

    def load_model(self, name):
        """

        :param name:
        """
        self.__model = load_model(name)

    def clear_session(self):
        """

        """
        clear_session()

    def compile(self, loss, optimizer, metrics=None):
        """

        :param loss:
        :param optimizer:
        :param metrics:
        """
        self.__model.compile(optimizer=optimizer,
                             loss=loss,
                             metrics=metrics)

    def __save_model(self, model, name):
        save_model(model=model, name=name)

    def __load_model(self, name):
        return load_model(name=name)
