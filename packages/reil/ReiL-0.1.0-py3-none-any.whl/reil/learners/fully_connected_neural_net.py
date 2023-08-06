# -*- coding: utf-8 -*-
'''
Dense class
===========

The Dense learner.
'''
import pathlib
from typing import Any, List, Optional, Tuple, Union

import numpy as np
import tensorflow as tf
from reil.datatypes.feature import FeatureArray
from reil.learners.learner import Learner
from reil.learners.learning_rate_schedulers import (ConstantLearningRate,
                                                    LearningRateScheduler)
from tensorflow import keras


class Dense_tf_1(Learner[float]):
    '''
    The Dense learner.

    This class uses `tf.keras` to build a sequential dense network with one
    output.
    '''

    def __init__(
            self,
            learning_rate: LearningRateScheduler,
            validation_split: float = 0.3,
            hidden_layer_sizes: Tuple[int, ...] = (1,),
            input_length: Optional[int] = None,
            tensorboard_path: Optional[Union[str, pathlib.PurePath]] = None,
            **kwargs: Any) -> None:
        '''
        Arguments
        ---------
        learning_rate:
            A `LearningRateScheduler` object that determines the learning rate
            based on iteration. If any scheduler other than constant is
            provided, the model uses the `new_rate` method of the scheduler
            to determine the learning rate at each iteration.

        validation_split:
            How much of the training set should be used for validation?

        hidden_layer_sizes:
            A list of number of neurons for each layer.

        input_length:
            Size of the input data. If not supplied, the network will be
            generated based on the size of the first data point in `predict` or
            `learn` methods.

        tensorboard_path:
            A path to save tensorboard outputs. If not provided,
            tensorboard will be disabled.

        Raises
        ------
        ValueError
            Validation split not in the range of (0.0, 1.0).
        '''

        super().__init__(learning_rate=learning_rate, **kwargs)

        self._iteration: int = 0

        self._hidden_layer_sizes = hidden_layer_sizes
        self._input_length = input_length

        if not 0.0 < validation_split < 1.0:
            raise ValueError('validation split should be in (0.0, 1.0).')

        self._validation_split = validation_split

        self._callbacks: List[Any] = []
        self._tensorboard_path: Optional[pathlib.PurePath] = None
        self._model: keras.models.Sequential

        self._graph = tf.Graph()
        with self._graph.as_default():
            self._session = tf.Session()  # type: ignore

            self._model = keras.models.Sequential()

            if tensorboard_path is not None:
                self._tensorboard_path = pathlib.PurePath(
                    'logs', tensorboard_path)
                self._tensorboard = keras.callbacks.TensorBoard(
                    log_dir=self._tensorboard_path)
                # , histogram_freq=1)  #, write_images=True)
                self._callbacks.append(self._tensorboard)

            if not isinstance(self._learning_rate,
                              ConstantLearningRate):
                learning_rate_scheduler = \
                    keras.callbacks.LearningRateScheduler(
                        self._learning_rate.new_rate, verbose=0)
                self._callbacks.append(learning_rate_scheduler)

        self._ann_ready: bool = False
        if self._input_length is not None:
            self._generate_network()

    def _generate_network(self) -> None:
        '''
        Generate a multilayer neural net using `keras.Dense`.
        '''

        with self._graph.as_default():
            self._model = keras.models.Sequential()
            self._model.add(
                keras.layers.Dense(self._hidden_layer_sizes[0],
                                   activation='relu',
                                   name='layer_01',
                                   input_shape=(self._input_length,)))
            for i, v in enumerate(self._hidden_layer_sizes[1:]):
                self._model.add(keras.layers.Dense(
                    v, activation='relu', name=f'layer_{i+2:0>2}'))

            self._model.add(keras.layers.Dense(1, name='output'))

            self._model.compile(optimizer=keras.optimizers.Adam(
                learning_rate=self._learning_rate.initial_lr), loss='mae')

        self._ann_ready = True

    def predict(self, X: Tuple[FeatureArray, ...]) -> Tuple[float, ...]:
        '''
        predict `y` for a given input list `X`.

        Arguments
        ---------
        X:
            A list of `FeatureArray` as inputs to the prediction model.

        Returns
        -------
        :
            The predicted `y`.
        '''
        _X: List[List[Any]] = [x.normalized.flatten() for x in X]
        if not self._ann_ready:
            self._input_length = len(_X[0])
            self._generate_network()

        with self._session.as_default():
            with self._graph.as_default():
                result = self._model.predict(np.array(_X))  # type: ignore

        return result  # type: ignore

    def learn(self, X: Tuple[FeatureArray, ...], Y: Tuple[float, ...]) -> None:
        '''
        Learn using the training set `X` and `Y`.

        Arguments
        ---------
        X:
            A list of `FeatureArray` as inputs to the learning model.

        Y:
            A list of float labels for the learning model.
        '''
        _X: List[List[Any]] = [x.normalized.flatten() for x in X]
        if not self._ann_ready:
            self._input_length = len(_X[0])
            self._generate_network()

        with self._session.as_default():
            with self._graph.as_default():
                self._model.fit(
                    np.array(_X), np.array(Y),
                    initial_epoch=self._iteration, epochs=self._iteration+1,
                    callbacks=self._callbacks,
                    validation_split=self._validation_split,
                    verbose=0)

    def reset(self) -> None:
        '''
        reset the learner.
        '''
        self._iteration += 1

    def save(self,
             filename: Optional[str] = None,
             path: Optional[Union[str, pathlib.PurePath]] = None,
             data_to_save: Optional[Tuple[str, ...]] = None
             ) -> Tuple[pathlib.PurePath, str]:
        '''
        Extends `ReilBase.save` to handle `TF` objects.

        Arguments
        ---------
        filename:
            the name of the file to be saved.

        path:
            the path in which the file should be saved.

        data_to_save:
            This argument is only present for signature consistency. It has
            no effect on save.

        Returns
        -------
        :
            a `Path` object to the location of the saved file and its name
            as `str`
        '''
        p, f = super().save(
            filename, path,
            tuple(attr for attr in self.__dict__.keys()
                  if attr not in ('_session', '_graph', '_model')))

        with self._session.as_default():
            with self._graph.as_default():
                self._model.save(p / f'{f}.tf')

        return p, f

    def load(self,
             filename: str,
             path: Optional[Union[str, pathlib.PurePath]] = None) -> None:
        '''
        Extends `ReilBase.load` to handle `TF` objects.

        Arguments
        ---------
        filename:
            The name of the file to be loaded.

        path:
            Path of the location of the file.

        Raises
        ------
        ValueError:
            The filename is not specified.
        '''
        super().load(filename, path)

        _path = path or '.'
        self._graph = tf.Graph()  # type: ignore
        with self._graph.as_default():
            self._session = keras.backend.get_session()
            self._model = keras.models.load_model(
                pathlib.Path(_path, f'{filename}.tf'))

            self._tensorboard = keras.callbacks.TensorBoard(
                log_dir=self._tensorboard_path)

            if not isinstance(self._learning_rate,
                              ConstantLearningRate):
                learning_rate_scheduler = \
                    keras.callbacks.LearningRateScheduler(
                        self._learning_rate.new_rate, verbose=0)
                self._callbacks.append(learning_rate_scheduler)


class Dense_tf_2(Learner[float]):
    '''
    The Dense learner.

    This class uses `tf.keras` to build a sequential dense network with one
    output.
    '''

    def __init__(
            self,
            learning_rate: LearningRateScheduler,
            validation_split: float = 0.3,
            hidden_layer_sizes: Tuple[int, ...] = (1,),
            input_length: Optional[int] = None,
            tensorboard_path: Optional[Union[str, pathlib.PurePath]] = None,
            **kwargs: Any) -> None:
        '''
        Arguments
        ---------
        learning_rate:
            A `LearningRateScheduler` object that determines the learning rate
            based on iteration. If any scheduler other than constant is
            provided, the model uses the `new_rate` method of the scheduler
            to determine the learning rate at each iteration.

        validation_split:
            How much of the training set should be used for validation?

        hidden_layer_sizes:
            A list of number of neurons for each layer.

        input_length:
            Size of the input data. If not supplied, the network will be
            generated based on the size of the first data point in `predict` or
            `learn` methods.

        tensorboard_path:
            A path to save tensorboard outputs. If not provided,
            tensorboard will be disabled.

        Raises
        ------
        ValueError
            Validation split not in the range of (0.0, 1.0).
        '''

        super().__init__(learning_rate=learning_rate, **kwargs)

        self._iteration: int = 0

        self._hidden_layer_sizes = hidden_layer_sizes
        self._input_length = input_length

        if not 0.0 < validation_split < 1.0:
            raise ValueError('validation split should be in (0.0, 1.0).')

        self._validation_split = validation_split

        self._callbacks: List[Any] = []
        self._tensorboard_path: Optional[pathlib.PurePath] = None
        self._model = keras.models.Sequential()

        if tensorboard_path is not None:
            self._tensorboard_path = pathlib.PurePath(
                'logs', tensorboard_path)
            self._tensorboard = keras.callbacks.TensorBoard(
                log_dir=self._tensorboard_path)
            # , histogram_freq=1)  #, write_images=True)
            self._callbacks.append(self._tensorboard)

        if not isinstance(self._learning_rate,
                          ConstantLearningRate):
            learning_rate_scheduler = \
                keras.callbacks.LearningRateScheduler(
                    self._learning_rate.new_rate, verbose=0)
            self._callbacks.append(learning_rate_scheduler)

        self._ann_ready: bool = False
        if self._input_length is not None:
            self._generate_network()

    def _generate_network(self) -> None:
        '''
        Generate a multilayer neural net using `keras.Dense`.
        '''
        self._model = keras.models.Sequential()
        self._model.add(
            keras.layers.Dense(self._hidden_layer_sizes[0],
                               activation='relu',
                               name='layer_01',
                               input_shape=(self._input_length,)))
        for i, v in enumerate(self._hidden_layer_sizes[1:]):
            self._model.add(keras.layers.Dense(
                v, activation='relu', name=f'layer_{i+2:0>2}'))

        self._model.add(keras.layers.Dense(1, name='output'))

        self._model.compile(optimizer=keras.optimizers.Adam(
            learning_rate=self._learning_rate.initial_lr), loss='mae')

        self._ann_ready = True

    def predict(self, X: Tuple[FeatureArray, ...]) -> Tuple[float, ...]:
        '''
        predict `y` for a given input list `X`.

        Arguments
        ---------
        X:
            A list of `FeatureArray` as inputs to the prediction model.

        Returns
        -------
        :
            The predicted `y`.
        '''
        _X: List[List[Any]] = [x.normalized.flatten() for x in X]
        if not self._ann_ready:
            self._input_length = len(_X[0])
            self._generate_network()

        result = self._model.predict(np.array(_X))

        return result  # type: ignore

    def learn(self, X: Tuple[FeatureArray, ...], Y: Tuple[float, ...]) -> None:
        '''
        Learn using the training set `X` and `Y`.

        Arguments
        ---------
        X:
            A list of `FeatureArray` as inputs to the learning model.

        Y:
            A list of float labels for the learning model.
        '''
        _X: List[List[Any]] = [x.normalized.flatten() for x in X]
        if not self._ann_ready:
            self._input_length = len(_X[0])
            self._generate_network()

        self._model.fit(
            np.array(_X), np.array(Y),
            initial_epoch=self._iteration, epochs=self._iteration+1,
            callbacks=self._callbacks,
            validation_split=self._validation_split,
            verbose=0)

    def reset(self) -> None:
        '''
        reset the learner.
        '''
        self._iteration += 1

    def save(self,
             filename: Optional[str] = None,
             path: Optional[Union[str, pathlib.PurePath]] = None,
             data_to_save: Optional[Tuple[str, ...]] = None
             ) -> Tuple[pathlib.PurePath, str]:
        '''
        Extends `ReilBase.save` to handle `TF` objects.

        Arguments
        ---------
        filename:
            the name of the file to be saved.

        path:
            the path in which the file should be saved.

        data_to_save:
            This argument is only present for signature consistency. It has
            no effect on save.

        Returns
        -------
        :
            a `Path` object to the location of the saved file and its name
            as `str`
        '''
        p, f = super().save(
            filename, path,
            tuple(attr for attr in self.__dict__.keys()
                  if attr not in ('_session', '_graph', '_model')))

        try:
            self._model.save(pathlib.Path(p, f'{f}.tf').resolve())
        except ValueError:
            self._logger.warning(
                'Model is not compiled. Skipped saving the model.')

        return p, f

    def load(self,
             filename: str,
             path: Optional[Union[str, pathlib.PurePath]] = None) -> None:
        '''
        Extends `ReilBase.load` to handle `TF` objects.

        Arguments
        ---------
        filename:
            The name of the file to be loaded.

        path:
            Path of the location of the file.

        Raises
        ------
        ValueError:
            The filename is not specified.
        '''
        super().load(filename, path)

        _path = path or '.'
        if self._ann_ready:
            self._model = keras.models.load_model(
                pathlib.Path(_path, f'{filename}.tf'))
        else:
            self._model = keras.models.Sequential()

        self._tensorboard = keras.callbacks.TensorBoard(
            log_dir=self._tensorboard_path)

        if not isinstance(self._learning_rate,
                          ConstantLearningRate):
            learning_rate_scheduler = \
                keras.callbacks.LearningRateScheduler(
                    self._learning_rate.new_rate, verbose=0)
            self._callbacks.append(learning_rate_scheduler)


if tf.__version__[0] == '1':  # type: ignore
    Dense = Dense_tf_1
else:
    Dense = Dense_tf_2
