# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pillow",
#     "requests",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    X = np.array([10, 10, 80, 10, 10, 10])
    K = np.array([-1, 0, 1])
    return K, X, np


@app.cell
def _(K, X, np):
    # Pad X with zeros on both sides to handle boundary
    n_conv = len(X) - len(K) + 1  # Now we get full length output
    XKconv = np.zeros(n_conv)

    for i in range(n_conv):
        XKconv[i] = np.sum(X[i:(i+len(K))] * K[::-1]) # Reverse the kernel and take element-wise product and sum up
    XKconv
    return


@app.cell
def _(K, X, np):
    # Step 1: Transform X and K to frequency domain
    FX = np.fft.fft(X)
    # Pad K with zeros to match the length of X before FFT
    K_padded = np.pad(K, (0, len(X) - len(K)), 'constant') # [-1  0  1  0  0  0]
    FK = np.fft.fft(K_padded)
    print("FX:", FX)
    return FK, FX


@app.cell
def _(FK, FX):
    FXKconv = FX * FK
    return (FXKconv,)


@app.cell
def _(FXKconv, np):
    XKconv_ft = np.real(np.fft.ifft(FXKconv))
    XKconv_ft
    return (XKconv_ft,)


@app.cell
def _(XKconv_ft):
    XKconv_ft_1 = XKconv_ft[2:]
    XKconv_ft_1
    return


@app.cell
def _(np):
    import matplotlib.pyplot as plt

    def basis_function(img_size=256, u=0, v=0):
        """
      img_size : square size of image f(x,y)
      u,v : spatial space indice
      """
        N = img_size
        x = np.linspace(0, N - 1, N)
        y = np.linspace(0, N - 1, N)
        x_, y_ = np.meshgrid(x, y)
        bf = np.exp(-1j * 2 * np.pi * (u * x_ / N + v * y_ / N))
        if u == 0 and v == 0:
            bf = np.round(bf)
        real = np.real(bf)
        _imag = np.imag(bf)
        return (real, _imag)
    size = 16
    _bf_arr_real = np.zeros((size * size, size, size))
    bf_arr_imag = np.zeros((size * size, size, size))
    _ind = 0
    for _col in range(size):
        for _row in range(size):
            _re, _imag = basis_function(img_size=size, u=_row, v=_col)
            _bf_arr_real[_ind] = _re
            bf_arr_imag[_ind] = _imag
            _ind = _ind + 1
    _, _axs = plt.subplots(size, size, figsize=(7, 7))
    _axs = _axs.flatten()
    for _img, _ax in zip(_bf_arr_real, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    return basis_function, bf_arr_imag, plt, size


@app.cell
def _(bf_arr_imag, plt, size):
    # imaginary part
    _, _axs = plt.subplots(size, size, figsize=(7, 7))
    _axs = _axs.flatten()
    for _img, _ax in zip(bf_arr_imag, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    return


@app.cell
def _(np, plt):
    from PIL import Image
    import requests
    from io import BytesIO

    def read_jpeg_from_url(url):
        response = requests.get(url)
        _img = Image.open(BytesIO(response.content))
        if _img.mode != 'RGB':
            _img = _img.convert('RGB')
        return _img

    def image_to_numpy(img):
        return np.array(_img)

    def to_gray_scale(img_np):
        return np.mean(img_np, axis=2)
    url = 'https://www.binghamton.edu/news/images/uploads/features/20180815_peacequad02_jwc.jpg'
    _img = read_jpeg_from_url(url)
    img_np = image_to_numpy(_img)
    img_gray = to_gray_scale(img_np)
    plt.imshow(img_gray, cmap='gray')
    return (img_gray,)


@app.cell
def _(img_gray, np):
    ft_img_gray = np.fft.fft2(img_gray)
    return (ft_img_gray,)


@app.cell
def _(ft_img_gray, np, plt):
    import matplotlib
    weight = np.abs(ft_img_gray)
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.imshow(weight, cmap='gray', norm=matplotlib.colors.LogNorm(), aspect='equal')
    # real part
    _cbar = fig1.colorbar(ax1.images[0], ax=ax1, orientation='horizontal')
    _cbar.set_label('Fourier transform magnitude')
    return


@app.cell
def _(basis_function, np, plt):
    size_1 = 16
    _bf_arr_real = np.zeros((size_1 * size_1, size_1, size_1))
    bf_arr_imag_1 = np.zeros((size_1 * size_1, size_1, size_1))
    _ind = 0
    for _col in range(-size_1 // 2, size_1 // 2):
        for _row in range(-size_1 // 2, size_1 // 2):
            _re, _imag = basis_function(img_size=size_1, u=_row, v=_col)
            _bf_arr_real[_ind] = _re
            bf_arr_imag_1[_ind] = _imag
            _ind = _ind + 1
    fig, _axs = plt.subplots(size_1, size_1, figsize=(7, 7))
    _axs = _axs.flatten()
    for _img, _ax in zip(_bf_arr_real, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    fig.suptitle('Real Part of Basis Functions')
    fig, _axs = plt.subplots(size_1, size_1, figsize=(7, 7))
    _axs = _axs.flatten()
    for _img, _ax in zip(bf_arr_imag_1, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    fig.suptitle('Imaginary Part of Basis Functions')
    return


@app.cell
def _(img_gray, np):
    K_1 = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])  # Prewitt operator
    K_padd = np.zeros((img_gray.shape[0], img_gray.shape[1]))
    K_padd[:K_1.shape[0], :K_1.shape[1]] = K_1
    # convolution
    FK_1 = np.fft.fft2(K_padd)
    return (FK_1,)


@app.cell
def _(FK_1, np, plt):
    plt.imshow(np.abs(FK_1), cmap='gray')
    _cbar = plt.colorbar()
    return


@app.cell
def _(FK_1, img_gray, np, plt):
    FX_1 = np.fft.fft2(img_gray)
    conv_img_gray = np.real(np.fft.ifft2(FX_1 * FK_1))
    plt.imshow(conv_img_gray, cmap='gray')
    return


if __name__ == "__main__":
    app.run()
