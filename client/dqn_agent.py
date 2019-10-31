import util
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
from collections import deque
import numpy as np


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.discount_rate = 0.95
        self.exploration_rate = 1.0  # exploration rate
        self.exploration_rate_min = 0.01
        self.exploration_rate_decay = 0.995
        self.learning_rate = 0.7
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.load_weights('model.h5')

        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            rand = random.randrange(self.action_size)
            return rand
        act_values = self.model.predict(state)
        max = np.argmax(act_values[0])

        return max

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            batch_size = len(self.memory)

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = reward + self.discount_rate * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration_rate > self.exploration_rate_min:
            self.exploration_rate *= self.exploration_rate_decay

    def save(self, filename=None):
        f = ('model.h5' if filename is None else filename)
        self.model.save_weights(f)


def get_agent(state_size, action_size):
    return DQNAgent(state_size, action_size)
