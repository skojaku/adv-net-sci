"""Regenerate the static figures for this module.

Extracted from docs/lecture-note/m09-graph-neural-networks/00-preparation.qmd.
Run from the repository root; writes SVGs into docs/lecture-note/figs/.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)


def _save(name):
    plt.savefig(OUT / f'{name}.svg', bbox_inches='tight', transparent=True)
    plt.close('all')
    print('wrote', name + '.svg')


# --- cell 0 --------------------------------------------------
import numpy as np
X = np.array([10, 10, 80, 10, 10, 10])
K = np.array([-1, 0, 1])

# --- cell 1 --------------------------------------------------
# Pad X with zeros on both sides to handle boundary
n_conv = len(X) - len(K) + 1  # Now we get full length output
XKconv = np.zeros(n_conv)

for i in range(n_conv):
    XKconv[i] = np.sum(X[i:(i+len(K))] * K[::-1]) # Reverse the kernel and take element-wise product and sum up
XKconv

# --- cell 2 --------------------------------------------------
# Step 1: Transform X and K to frequency domain
FX = np.fft.fft(X)
# Pad K with zeros to match the length of X before FFT
K_padded = np.pad(K, (0, len(X) - len(K)), 'constant') # [-1  0  1  0  0  0]
FK = np.fft.fft(K_padded)
print("FX:", FX)

# --- cell 3 --------------------------------------------------
FXKconv = FX * FK

# --- cell 4 --------------------------------------------------
XKconv_ft = np.real(np.fft.ifft(FXKconv))
XKconv_ft

# --- cell 5 --------------------------------------------------
XKconv_ft = XKconv_ft[2:]
XKconv_ft

# --- cell 6 --------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def basis_function(img_size=256, u=0, v=0):
  '''
  img_size : square size of image f(x,y)
  u,v : spatial space indice
  '''
  N = img_size
  x = np.linspace(0, N-1, N)
  y = np.linspace(0, N-1, N)
  x_, y_ = np.meshgrid(x, y)
  bf = np.exp(-1j*2*np.pi*(u*x_/N+v*y_/N))
  if u == 0 and v == 0:
    bf = np.round(bf)
  real = np.real(bf) # The cosine part
  imag = np.imag(bf) # The sine part
  return real, imag

size = 16
bf_arr_real = np.zeros((size*size,size,size))
bf_arr_imag = np.zeros((size*size,size,size))
ind = 0
for col in range(size):
  for row in range(size):
    re,imag = basis_function(img_size=size, u=row, v=col)
    bf_arr_real[ind] = re
    bf_arr_imag[ind] = imag
    ind += 1

# real part
_, axs = plt.subplots(size, size, figsize=(7, 7))
axs = axs.flatten()
for img, ax in zip(bf_arr_real, axs):
  ax.set_axis_off()
  ax.imshow(img,cmap='gray')
_save('m09prep-fig-00')

# --- cell 7 --------------------------------------------------
# imaginary part
_, axs = plt.subplots(size, size, figsize=(7, 7))
axs = axs.flatten()
for img, ax in zip(bf_arr_imag, axs):
  ax.set_axis_off()
  ax.imshow(img,cmap='gray')
_save('m09prep-fig-01')

# --- cell 8 --------------------------------------------------
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

# Read image from URL
def read_jpeg_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # Convert to RGB mode if needed (in case it's RGBA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img

def image_to_numpy(img):
    return np.array(img)

def to_gray_scale(img_np):
    return np.mean(img_np, axis=2)

# URL of the image
url = "https://www.binghamton.edu/news/images/uploads/features/20180815_peacequad02_jwc.jpg"

img = read_jpeg_from_url(url)
img_np = image_to_numpy(img)
img_gray = to_gray_scale(img_np)

plt.imshow(img_gray, cmap='gray')
_save('m09prep-fig-02')

# --- cell 9 --------------------------------------------------
ft_img_gray = np.fft.fft2(img_gray)

# --- cell 10 --------------------------------------------------
import matplotlib

weight = np.abs(ft_img_gray)

# real part
fig1, ax1 = plt.subplots(figsize=(5, 5))

ax1.imshow(weight, cmap='gray', norm=matplotlib.colors.LogNorm(), aspect='equal')
cbar = fig1.colorbar(ax1.images[0], ax=ax1, orientation='horizontal')
cbar.set_label('Fourier transform magnitude')
_save('m09prep-fig-03')

# --- cell 11 --------------------------------------------------
size = 16
bf_arr_real = np.zeros((size*size,size,size))
bf_arr_imag = np.zeros((size*size,size,size))
ind = 0
for col in range(-size//2, size//2):
  for row in range(-size//2, size//2):
    re,imag = basis_function(img_size=size, u=row, v=col)
    bf_arr_real[ind] = re
    bf_arr_imag[ind] = imag
    ind += 1

# real part
fig, axs = plt.subplots(size, size, figsize=(7, 7))
axs = axs.flatten()
for img, ax in zip(bf_arr_real, axs):
  ax.set_axis_off()
  ax.imshow(img,cmap='gray')

fig.suptitle('Real Part of Basis Functions')


# imaginary part
fig, axs = plt.subplots(size, size, figsize=(7, 7))
axs = axs.flatten()
for img, ax in zip(bf_arr_imag, axs):
  ax.set_axis_off()
  ax.imshow(img,cmap='gray')

fig.suptitle('Imaginary Part of Basis Functions')
_save('m09prep-fig-04')

# --- cell 12 --------------------------------------------------
K = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]) # Prewitt operator

K_padd = np.zeros((img_gray.shape[0], img_gray.shape[1]))
K_padd[:K.shape[0], :K.shape[1]] = K

# convolution
FK = np.fft.fft2(K_padd)

# --- cell 13 --------------------------------------------------
plt.imshow(np.abs(FK), cmap='gray')
cbar = plt.colorbar()
_save('m09prep-fig-05')

# --- cell 14 --------------------------------------------------
FX = np.fft.fft2(img_gray)
conv_img_gray = np.real(np.fft.ifft2(FX * FK))
plt.imshow(conv_img_gray, cmap='gray')
_save('m09prep-fig-06')
