import os
import random
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    画面内判定
    """
    yoko, tate = True, True

    if rct.left < 0 or rct.right > WIDTH:
        yoko = False

    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False

    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面表示
    """
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(180)

    cry_img = pg.transform.rotozoom(
        pg.image.load("fig/8.png"),
        0,
        1.5
    )

    left_rct = cry_img.get_rect()
    left_rct.center = (WIDTH//2-220, HEIGHT//2)

    right_rct = cry_img.get_rect()
    right_rct.center = (WIDTH//2+220, HEIGHT//2)

    font = pg.font.Font(None, 90)

    txt = font.render(
        "Game Over",
        True,
        (255, 255, 255)
    )

    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2, HEIGHT//2)

    screen.blit(black, (0, 0))
    screen.blit(cry_img, left_rct)
    screen.blit(cry_img, right_rct)
    screen.blit(txt, txt_rct)

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾画像リストと加速度リスト生成
    """
    bb_imgs = []

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(
            bb_img,
            (255, 0, 0),
            (10*r, 10*r),
            10*r
        )
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs


def init_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動方向とこうかとん画像の辞書生成
    """
    org_img = pg.transform.rotozoom(
        pg.image.load("fig/3.png"),0,0.9)

    right_img = pg.transform.flip(org_img, True, False)

    return {
        (0, 0): org_img,

        # 右
        (+5, 0): right_img,

        # 右上
        (+5, -5): pg.transform.rotozoom(right_img, 45, 1.0),

        # 上
        (0, -5): pg.transform.rotozoom(org_img, -90, 1.0),

        # 左上
        (-5, -5): pg.transform.rotozoom(org_img, -45, 1.0),

        # 左
        (-5, 0): org_img,

        # 左下
        (-5, +5): pg.transform.rotozoom(org_img, 45, 1.0),

        # 下
        (0, +5): pg.transform.rotozoom(org_img, 90, 1.0),

        # 右下
        (+5, +5): pg.transform.rotozoom(right_img, -45, 1.0),
    }


def main():
    pg.display.set_caption("逃げろ！こうかとん")

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとん画像辞書
    kk_imgs = init_kk_imgs()
    kk_img = kk_imgs[(0, 0)]

    kk_rct = kk_img.get_rect()
    kk_rct.center = (300, 200)

    # 爆弾画像リスト
    bb_imgs, bb_accs = init_bb_imgs()

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()

    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, (0, 0))

        # キー入力
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # 向き変更
        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]

        # 移動
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)

        # 爆弾サイズ・速度変更
        idx = min(tmr // 500, 9)

        bb_img = bb_imgs[idx]

        center = bb_rct.center

        bb_rct = bb_img.get_rect(center=center)

        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)

        if not yoko:
            vx *= -1

        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()