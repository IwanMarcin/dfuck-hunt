def main(mode=None):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    player = Player(gun_idle, gun_frames, HEIGHT)
    enemies = [DfuckVurnelable(HEIGHT, WIDTH) if random.random() < 0.7 else DfuckArmed(HEIGHT, WIDTH, poop) for _ in range(5)]

    run = True
    while run:
        clock.tick(FPS)
        enemies_to_remove = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()

                for enemy in enemies:
                    if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                        if isinstance(enemy, DfuckVurnelable):
                            enemy.dfuck_die(player, dfuck_die_frames)
                        elif isinstance(enemy, DfuckArmed):
                            enemy.dfuck_die(player, dfuck_armed_die_frames)
                        quack_sound.play()
                        enemies_to_remove.append(enemy)
                        break
            
            if len(enemies) < 5:
                if random.random() < 0.5:
                    enemies.append(DfuckVurnelable(HEIGHT, WIDTH))
                else:
                    enemies.append(DfuckArmed(HEIGHT, WIDTH, poop))
        
        for enemy in enemies:
            enemy.move()

        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        screen.blit(background, (0, 0))

        for enemy in enemies:
            if isinstance(enemy, DfuckVurnelable):
                enemy.draw(screen, dfuck_frames)
            else:
                enemy.draw(screen, dfuck_armed_frames)

        player.update()
        

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() // 2,
                                mouse_pos[1] - crosshair.get_height() // 2))
        
        txt = f"HP: {player.hp:.0f}% Hits: {player.hits} Shoots: {player.shots}"

        screen.blit(FONT.render(txt, True, (255, 255, 255)), (10, 10))
        player.draw(screen)
        pygame.display.update()