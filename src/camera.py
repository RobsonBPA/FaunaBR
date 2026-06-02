def atualizar_camera(player_x, player_y, tela_lar, tela_alt, mapa_lar, mapa_alt):
    
    camera_x = player_x - tela_lar // 2
    camera_y = player_y - tela_alt // 2

    camera_x = max(0, min(camera_x, mapa_lar - tela_lar))
    camera_y = max(0, min(camera_y, mapa_alt - tela_alt))

    return camera_x, camera_y