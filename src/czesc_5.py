from src.czesc_4 import *

seed = 42

def gradienty_losowo_wygeneruj_v1(dtg, w_min, w_max, seed):
    rng = np.random.default_rng(seed)
    return rng.uniform(low=w_min, high=w_max, size=(dtg, 2))

def szum_PerlinaPlus2d_przygotuj(dtw, wys_min, wys_max, dtg, grad_xy_min, grad_xy_max, seed):
    random.seed(seed)
    tab_wys = [random.uniform(wys_min, wys_max) for _ in range(dtw)]
    tab_perm_wys = permutacje_podw_wygeneruj_v1(dtw, seed)
    tab_grad = gradienty_losowo_wygeneruj_v1(dtg, grad_xy_min, grad_xy_max, seed)
    tab_perm_grad = permutacje_podw_wygeneruj_v1(dtg, seed + 1)
    return tab_wys, tab_perm_wys, tab_grad, tab_perm_grad

def interpolacja_2d_rdzen_PerlinaPlus(grad_ld, grad_lg, grad_pd, grad_pg, wys_ld, wys_lg, wys_pd, wys_pg, delta_x, delta_y):
    fade_x = 6 * math.pow(delta_x, 5) - 15 * math.pow(delta_x, 4) + 10 * math.pow(delta_x, 3)
    fade_y = 6 * math.pow(delta_y, 5) - 15 * math.pow(delta_y, 4) + 10 * math.pow(delta_y, 3)
    return (
            (wys_ld + np.dot(np.array([delta_x, delta_y]), grad_ld)) * (1 - fade_x) * (1 - fade_y) +
            (wys_lg + np.dot(np.array([delta_x, delta_y - 1]), grad_lg)) * (1 - fade_x) * fade_y +
            (wys_pd + np.dot(np.array([delta_x - 1, delta_y]), grad_pd)) * fade_x * (1 - fade_y) +
            (wys_pg + np.dot(np.array([delta_x - 1, delta_y - 1]), grad_pg)) * fade_x * fade_y
    )

def szum_2d_PerlinaPlus_vperm3(x, y, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys):
    x_l = math.floor(x)
    x_p = x_l + 1
    y_d = math.floor(y)
    y_g = y_d + 1
    delta_x = x - x_l
    delta_y = y - y_d
    i_wys_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm_wys)
    i_wys_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm_wys)
    i_wys_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm_wys)
    i_wys_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm_wys)
    wys_ld = tab_wys[i_wys_ld]
    wys_lg = tab_wys[i_wys_lg]
    wys_pd = tab_wys[i_wys_pd]
    wys_pg = tab_wys[i_wys_pg]
    i_grad_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm_grad)
    i_grad_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm_grad)
    i_grad_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm_grad)
    i_grad_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm_grad)
    grad_ld = tab_grad[i_grad_ld]
    grad_lg = tab_grad[i_grad_lg]
    grad_pd = tab_grad[i_grad_pd]
    grad_pg = tab_grad[i_grad_pg]
    return interpolacja_2d_rdzen_PerlinaPlus(grad_ld, grad_lg, grad_pd, grad_pg, wys_ld, wys_lg, wys_pd, wys_pg, delta_x, delta_y)

if __name__ == "__main__":
    def test_szum_PerlinaPlus2d_przygotuj():
        tab_wys, tab_perm_wys, tab_grad, tab_perm_grad = szum_PerlinaPlus2d_przygotuj(5, 0, 1, 4, -1, +1, seed)
        print(tab_wys)
        print(tab_perm_wys)
        print(tab_grad)
        print(tab_perm_grad)

    #test_szum_PerlinaPlus2d_przygotuj()

    def test_interpolacja_2d_rdzen_PerlinaPlus():
        x = np.arange(0, 1, .1)
        y = np.arange(0, 1, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_rdzen_PerlinaPlus([0, 0], [0, -2], [1, 1], [-2, 0], 0, 1, 3, 2, X[i, j], Y[i, j])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_interpolacja_2d_rdzen_PerlinaPlus()

    def test_szum_2d_PerlinaPlus_vperm3():
        x = np.arange(-1, 3, .1)
        y = np.arange(2, 4, .1)
        tab_wys = [0, .25, .5, .75, 1]
        tab_perm_wys = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]
        tab_perm_grad = [3, 2, 0, 1, 3, 2, 0, 1]
        tab_grad = np.array([
            [-0.80, -0.33],
            [ 0.00,  0.40],
            [-0.45,  0.39],
            [ 0.64,  0.13]
        ])

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = szum_2d_PerlinaPlus_vperm3(X[i, j], Y[i, j], tab_grad, tab_perm_grad, tab_wys, tab_perm_wys)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_szum_2d_PerlinaPlus_vperm3()

    # <--- Ćwiczenia --->
    def zadanie_1():
        test_szum_PerlinaPlus2d_przygotuj()

    zadanie_1()

    def zadanie_2():
        test_interpolacja_2d_rdzen_PerlinaPlus()

    zadanie_2()

    def zadanie_3():
        test_szum_2d_PerlinaPlus_vperm3()

    zadanie_3()