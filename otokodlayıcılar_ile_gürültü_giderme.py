# Kütüphane Kurulumları
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.callbacks import TensorBoard
from keras.datasets import mnist
import numpy as np
from keras import backend as K
import matplotlib.pyplot as plt

# Veri Kümesini Oluşturup ayırmak
(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

x_train = np.reshape (x_train, (len(x_train), 28, 28, 1))
x_test =  np.reshape (x_test, (len(x_test), 28, 28, 1))
print('Eğtiim',x_train.shape)
print('Test', x_test.shape)

# Veriye Gürültü Ekleme Adımı
noise_factor = 0.5

x_train_noisy = x_train + noise_factor * np.random.normal(loc = 0.0, scale = 1.0, size = x_train.shape)
x_test_noisy = x_test + noise_factor * np.random.normal(loc = 0.0, scale = 1.0, size = x_test.shape)

x_train_noisy = np.clip(x_train_noisy, 0. ,1.)
x_test_noisy = np.clip(x_test_noisy, 0. ,1.)

# Gürültülü Veriyi Görselleştirme
n = 10

plt.figure(figsize = (25,4))

for i in range(n):
  ax = plt.subplot(2, n, i+1)
  plt.imshow(x_test_noisy[i].reshape(28,28))
  plt.gray()
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
plt.show()
print('gürültülü orijinal görüntüler')

# ENCODE Modeli

input_img = Input(shape = (28, 28, 1))

x = Conv2D(32, (3,3), activation='relu', padding='same')(input_img)

x = MaxPooling2D((2,2), padding='same')(x)

x = Conv2D(32, (3,3), activation='relu', padding='same')(x)

encoded = MaxPooling2D((2,2), padding='same')(x)

# (7, 7, 32)

# DECODE Modeli

x = Conv2D(32, (3,3), activation='relu', padding='same')(encoded)

x = UpSampling2D((2,2))(x)

x = Conv2D(32, (3,3), activation='relu', padding='same')(x)

x = UpSampling2D((2,2))(x)

decoded = Conv2D(1, (3,3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

# Modelin Derlenmesi ve Eğitilmesi

autoencoder.fit(x_train_noisy, x_train,
                epochs=10,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test_noisy, x_test),
                callbacks=[TensorBoard(log_dir='/tmp/tb', histogram_freq=0, write_graph=False)])

decoded_imgs = autoencoder.predict(x_test)

# Sonuçların Görselleştirilmesi
# (Burada epoch sayısı 10 olduğu için sonuçlar tam olarak istediğimiz gibi olmayabilir ancak siz isterseniz epoch sayısını 100 e çıkarıp daha net görseller elde edebilirsiniz. Genel mantık bu şekildedir.)

n = 10
plt.figure(figsize=(25, 4))
for i in range(n):
    # Yeniden yapılandırmayı ekranda göster.
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()
print("DENOISED _ GÜRÜLTÜSÜ BASTIRILMIŞ GÖRÜNTÜ")
