import os
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
    引数：こうかとんRectまたは爆弾Rect
    戻り値：(横方向判定, 縦方向判定)
    True：画面内
    False：画面外
    """
    yoko, tate = True, True

    if rct.left < 0 or rct.right > WIDTH:
        yoko = False

    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False

    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する
    """
    # 半透明黒背景
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(180)

    # 泣きこうかとん（大きめ）
    cry_img = pg.transform.rotozoom(
        pg.image.load("fig/8.png"),
        0,
        1.5
    )

    # 左右配置
    left_rct = cry_img.get_rect()
    left_rct.center = (WIDTH // 2 - 220, HEIGHT // 2)

    right_rct = cry_img.get_rect()
    right_rct.center = (WIDTH // 2 + 220, HEIGHT // 2)

    # Game Over文字
    font = pg.font.Font(None, 90)

    txt = font.render(
        "Game Over",
        True,
        (255, 255, 255)
    )

    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)

    # 描画
    screen.blit(black, (0, 0))
    screen.blit(cry_img, left_rct)
    screen.blit(cry_img, right_rct)
    screen.blit(txt, txt_rct)

    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(
        pg.image.load("fig/3.png"),
        0,
        0.9
    )

    kk_rct = kk_img.get_rect()
    kk_rct.center = (300, 200)

    # 爆弾生成
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(
        bb_img,
        (255, 0, 0),
        (10, 10),
        10
    )
    bb_img.set_colorkey((0, 0, 0))

    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = 5, 5

    clock = pg.time.Clock()

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

        # こうかとん移動
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(
                -sum_mv[0],
                -sum_mv[1]
            )

        screen.blit(kk_img, kk_rct)

        # 爆弾移動
        bb_rct.move_ip(vx, vy)

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
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()