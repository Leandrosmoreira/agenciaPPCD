# video-009-anticristo — Phantasma MoviePy Script
# Abismo Criativo — gerado em 2026-04-13
# Agente: Phantasma — Editor Cinematografico
# Canal: Sinais do Fim — Passagens do Apocalipse

from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, concatenate_audioclips
)
import numpy as np
import os
import glob

# ==============================================================================
# CONFIGURACOES
# ==============================================================================

OUTPUT_PATH = "canais/sinais-do-fim/videos/video-009-anticristo/8-render/video-009-anticristo_v1.mp4"
IMAGES_DIR  = "canais/sinais-do-fim/videos/video-009-anticristo/7-imagens/"
AUDIO_DIR   = "canais/sinais-do-fim/videos/video-009-anticristo/5-audio/"
FPS         = 24
RESOLUTION  = (1920, 1080)
CROSSFADE   = 0.5   # segundos de crossfade entre clips

# Cores do canal (paleta dark)
VIGNETTE_STRENGTH = 0.55   # 0.0 = sem vinheta, 1.0 = borda totalmente preta
BRIGHTNESS_FACTOR = 0.90   # 0.90 = -10% de brilho
CONTRAST_FACTOR   = 1.15   # 1.15 = +15% de contraste

# ==============================================================================
# MAPEAMENTO DE IMAGENS — 90 quadros, 18 por parte
# Cada imagem eh mapeada ao quadro correspondente do storyboard.
# Os nomes sao os arquivos .png da pasta 7-imagens (sem diretorio base),
# listados na ordem exata do storyboard (Quadro 1 -> Quadro 90).
# Se uma imagem especifica nao existir, o script usa fallback ciclico.
# ==============================================================================

IMAGE_FILENAMES = [
    # --- PARTE 1 (Quadros 1-18) ---
    # Q1  angel_of_destruction
    "leandromoreira53._colorful_vivid_angel_of_destruction_in_deep_f95fcfb5-3ede-4adc-b813-12908d69f06f_3.png",
    # Q2  prophet_Daniel_sapphire
    "leandromoreira53._colorful_vivid_prophet_Daniel_in_sapphire_b_30d351e2-713d-485c-b35a-add23cfd0d37_3.png",
    # Q3  six-winged_seraph
    "leandromoreira53._colorful_vivid_six-winged_seraph_in_blazing_4b951709-e402-48c5-a9ab-556b52862c9a_1.png",
    # Q4  prophetess_Deborah
    "leandromoreira53._colorful_vivid_prophetess_Deborah_in_ochre__84f56bb6-5b63-4629-b4f2-3a2d4e19a211_1.png",
    # Q5  King_Solomon_crimson
    "leandromoreira53._colorful_vivid_King_Solomon_in_crimson_robe_5ebf73ca-1b7c-4542-a792-528ad398b7ce_3.png",
    # Q6  medieval_cartographer_angel
    "leandromoreira53._colorful_vivid_medieval_cartographer_angel__1f820918-0fcd-42fa-8771-02351bccc61d_2.png",
    # Q7  Horseman_of_the_Apocalypse
    "leandromoreira53._colorful_vivid_Horseman_of_the_Apocalypse_o_9f55f36a-477b-433b-baee-80460469f658_3.png",
    # Q8  prophet_Daniel_white_tunic
    "leandromoreira53._colorful_vivid_prophet_Daniel_in_white_tuni_a34d6f55-9c2b-4c72-b220-89209ba25083_2.png",
    # Q9  Moses_wine-red
    "leandromoreira53._colorful_vivid_Moses_in_deep_wine-red_and_o_25f0d5cf-b0b0-4df7-aeca-6d071449cd25_1.png",
    # Q10 balance_angel
    "leandromoreira53._colorful_vivid_balance_angel_in_gold_and_cr_5d1288a5-05b9-4854-b9e5-90a469a63ff5_3.png",
    # Q11 Ancient_of_Days
    "leandromoreira53._colorful_vivid_Ancient_of_Days_in_snow-whit_766b4ce4-61fc-468e-8eb8-420476977e72_3.png",
    # Q12 John_of_Patmos
    "leandromoreira53._colorful_vivid_John_of_Patmos_in_indigo_blu_a85c06c8-74d8-400a-bf9b-f09930cda0c5_3.png",
    # Q13 cherubim_four-faced (querubim)
    "leandromoreira53._colorful_vivid_all-seeing_cherubim_in_turqu_360921b2-cfed-4467-afdf-1b21407bc8eb_1.png",
    # Q14 prophet_Ezekiel
    "leandromoreira53._colorful_vivid_prophet_Ezekiel_in_moss-gree_9c19fe92-f838-4a05-96ae-20f0a4dc84cb_3.png",
    # Q15 Archangel_Gabriel_brilliant
    "leandromoreira53._colorful_vivid_Archangel_Gabriel_in_brillia_7df9b90d-290d-4a96-bf6b-d8fe521802d6_3.png",
    # Q16 medieval_high_priest_purple
    "leandromoreira53._colorful_vivid_medieval_high_priest_in_purp_cd9fde37-8317-432e-8f38-27d68212dd69_3.png",
    # Q17 hooded_figure_crimson
    "leandromoreira53._colorful_vivid_hooded_figure_in_deep_crimso_1d4b066b-2e84-432a-bd11-979521293579_2.png",
    # Q18 sealing_angel
    "leandromoreira53._colorful_vivid_sealing_angel_standing_on_li_4c7c1f01-453d-42ce-bc41-53afa06e9923_3.png",

    # --- PARTE 2 (Quadros 19-36) ---
    # Q19 young_prophet_Daniel_lapis
    "leandromoreira53._colorful_vivid_young_prophet_Daniel_in_lapi_8ede65f7-a866-4edf-9880-210cb4c10fb3_3.png",
    # Q20 ancient_high_priest_ivory
    "leandromoreira53._colorful_vivid_ancient_high_priest_in_ivory_c104090d-1c4c-427d-8273-4203f02574f3_3.png",
    # Q21 intercessor_angel_vivid_red
    "leandromoreira53._colorful_vivid_intercessor_angel_in_vivid_r_3c81cd50-5f8d-4f6e-9a1d-b91060e935da_3.png",
    # Q22 Babylonian_demon
    "leandromoreira53._colorful_vivid_Babylonian_demon_with_black__4942abcc-2274-450b-812f-f5077875758d_3.png",
    # Q23 King_Nebuchadnezzar
    "leandromoreira53._colorful_vivid_King_Nebuchadnezzar_in_golde_09cd6aff-98b6-4990-a2a1-17aaabc92e3b_3.png",
    # Q24 covenant_angel_royal_blue
    "leandromoreira53._colorful_vivid_covenant_angel_in_royal_blue_c8fcb52c-563e-4b9d-bf87-ad215b801f2d_3.png",
    # Q25 Hiram_of_Tyre
    "leandromoreira53._colorful_vivid_Hiram_of_Tyre_in_ochre_and_b_d3b05477-3001-4bd7-aaa6-8f99d32b77cb_3.png",
    # Q26 seven-headed_Beast
    "leandromoreira53._colorful_vivid_seven-headed_Beast_in_blood-_bef16b8b-19e6-4fe7-b5a6-ba03e3fb7c26_2.png",
    # Q27 Archangel_Gabriel_descending
    "leandromoreira53._colorful_vivid_Archangel_Gabriel_descending_e01f0017-cfba-4843-9bf0-41fc635c16b6_3.png",
    # Q28 patriarch_Abraham_bronze
    "leandromoreira53._colorful_vivid_patriarch_Abraham_in_bronze__645e587e-a2d9-4837-a624-534d6aec8979_3.png",
    # Q29 cartographer_angel_purple
    "leandromoreira53._colorful_vivid_cartographer_angel_in_purple_dbcd5a0a-355b-4bdf-9fa5-c41a10a6e14f_3.png",
    # Q30 aged_prophet_Daniel_royal
    "leandromoreira53._colorful_vivid_aged_prophet_Daniel_in_royal_a68d6514-4e51-45ce-86af-91403ab6ce45_3.png",
    # Q31 messenger_angel_gold
    "leandromoreira53._colorful_vivid_messenger_angel_in_gold_and__92c43e05-6510-44af-b7c7-5bbf06705426_2.png",
    # Q32 resurrected_Christ_radiant
    "leandromoreira53._colorful_vivid_resurrected_Christ_in_radian_6b00b688-8a98-4a4c-94ab-ca11f7c6b7ab_2.png",
    # Q33 judgment_angel
    "leandromoreira53._colorful_vivid_judgment_angel_with_raised_g_6942d338-ccd7-4915-b37b-0da0a4e7da60_3.png",
    # Q34 young_Babylonian_prince
    "leandromoreira53._colorful_vivid_young_Babylonian_prince_in_g_041facf5-b20d-4d2b-bb25-0ba9390c01cc_3.png",
    # Q35 mediator_angel_white
    "leandromoreira53._colorful_vivid_mediator_angel_in_white_and__08eed132-fa2a-45df-8959-82d6534cbce0_3.png",
    # Q36 architect_demon
    "leandromoreira53._colorful_vivid_architect_demon_with_black_w_3d44f80a-1e86-4f07-902c-a7d5395e9768_1.png",

    # --- PARTE 3 (Quadros 37-54) ---
    # Q37 King_Solomon_receiving_tribute_3
    "leandromoreira53._colorful_vivid_King_Solomon_receiving_tribu_06e2a2d5-5c14-499a-9778-e9849fa13254_3.png",
    # Q38 King_Solomon_receiving_tribute_2
    "leandromoreira53._colorful_vivid_King_Solomon_receiving_tribu_06e2a2d5-5c14-499a-9778-e9849fa13254_2.png",
    # Q39 Babylonian_royal_counselor
    "leandromoreira53._colorful_vivid_Babylonian_royal_counselor_i_df0efb54-3885-4147-8919-fee99a0f1ed3_2.png",
    # Q40 Persian_prince_turquoise
    "leandromoreira53._colorful_vivid_Persian_prince_in_turquoise__0cf4b758-b3f1-4c97-8b72-2cd949ed3e9a_2.png",
    # Q41 biblical_phoenix
    "leandromoreira53._colorful_vivid_biblical_phoenix_with_glowin_0ba5c8f6-875f-4770-bb40-1360bc8605e2_3.png",
    # Q42 oracle_white_amber_3
    "leandromoreira53._colorful_vivid_oracle_in_white_and_amber_ro_cc39c66c-f11d-4dfa-80d4-9670a9a7cc20_3.png",
    # Q43 witness_angel_jade_green
    "leandromoreira53._colorful_vivid_witness_angel_in_jade_green__53b121d4-fa7c-4ef1-9a7c-aa82ba0e79a1_1.png",
    # Q44 shadow_angel_jet-black
    "leandromoreira53._colorful_vivid_shadow_angel_in_jet-black_an_8d659418-f978-48f2-b477-e89c9debad02_2.png",
    # Q45 apocalyptic_prophetess_3
    "leandromoreira53._colorful_vivid_apocalyptic_prophetess_in_sc_a19f05a5-c3ba-4a50-841b-6c85d3f41069_3.png",
    # Q46 accountant_angel_sapphire
    "leandromoreira53._colorful_vivid_accountant_angel_in_sapphire_14c1a569-8589-43eb-9763-3ad301193d8d_3.png",
    # Q47 Babylonian_cosmic_spider
    "leandromoreira53._colorful_vivid_Babylonian_cosmic_spider_in__685573ee-d7b7-4ecb-95d3-4a4d69a2fbe3_1.png",
    # Q48 prophet_Daniel_deep_medit
    "leandromoreira53._colorful_vivid_prophet_Daniel_in_deep_medit_50142893-fc92-42c9-a25b-766db76bfdfe_0.png",
    # Q49 modern_Prometheus_incande_3
    "leandromoreira53._colorful_vivid_modern_Prometheus_in_incande_4b539ce8-9bcf-4f7e-8987-d6d34f2621c7_3.png",
    # Q50 two_war_angels_gold
    "leandromoreira53._colorful_vivid_two_war_angels_in_gold_and_c_aeca8054-92d8-43f2-9811-a6ed13d8aa66_2.png",
    # Q51 technological_Leviathan
    "leandromoreira53._colorful_vivid_technological_Leviathan_with_96d31298-6d78-4ec0-95e7-7c2684a2fdad_1.png",
    # Q52 destroying_angel_rust
    "leandromoreira53._colorful_vivid_destroying_angel_in_rust-gre_decae016-d4e6-43dc-942d-de93010cf1e8_3.png",
    # Q53 Croesus_of_Lydia
    "leandromoreira53._colorful_vivid_Croesus_of_Lydia_in_gold_arm_ff0edada-0827-4b6c-b602-2d0c3d561465_3.png",
    # Q54 two_warrior_prophets_gold
    "leandromoreira53._colorful_vivid_two_warrior_prophets_in_gold_3b639bf2-3f2c-4140-a3f4-99baf85d28ce_3.png",

    # --- PARTE 4 (Quadros 55-72) — Musk + Macron ---
    # Q55 European_medieval_king_3
    "leandromoreira53._colorful_vivid_European_medieval_king_in_Fr_21d1740f-4ea8-4664-b9ec-d06e046775c3_3.png",
    # Q56 Daniels_Beast_ten_horns
    "leandromoreira53._colorful_vivid_Daniels_Beast_with_ten_horns_750d7f0e-d316-46db-b06e-40e51fa63461_0.png",
    # Q57 revealer_angel_white_3
    "leandromoreira53._colorful_vivid_revealer_angel_in_white_and__e513e2cf-9f7f-4e9d-8448-9ecdd983a279_3.png",
    # Q58 Archangel_Michael_gold
    "leandromoreira53._colorful_vivid_Archangel_Michael_in_gold_an_47e8da05-fed1-4238-b87c-73102dc4aff0_2.png",
    # Q59 false_prophet_foam-white
    "leandromoreira53._colorful_vivid_false_prophet_in_foam-white__da590e89-d9ab-4752-897e-e059a92c2f9f_3.png",
    # Q60 angel_of_destruction_0 (variacao diferente do Q1)
    "leandromoreira53._colorful_vivid_angel_of_destruction_in_deep_f95fcfb5-3ede-4adc-b813-12908d69f06f_0.png",
    # Q61 prophet_Daniel_sapphire_2
    "leandromoreira53._colorful_vivid_prophet_Daniel_in_sapphire_b_30d351e2-713d-485c-b35a-add23cfd0d37_2.png",
    # Q62 prophet_Daniel_sapphire_0
    "leandromoreira53._colorful_vivid_prophet_Daniel_in_sapphire_b_30d351e2-713d-485c-b35a-add23cfd0d37_0.png",
    # Q63 King_Solomon_crimson_1
    "leandromoreira53._colorful_vivid_King_Solomon_in_crimson_robe_5ebf73ca-1b7c-4542-a792-528ad398b7ce_1.png",
    # Q64 medieval_cartographer_3
    "leandromoreira53._colorful_vivid_medieval_cartographer_angel__1f820918-0fcd-42fa-8771-02351bccc61d_3.png",
    # Q65 balance_angel_0
    "leandromoreira53._colorful_vivid_balance_angel_in_gold_and_cr_5d1288a5-05b9-4854-b9e5-90a469a63ff5_0.png",
    # Q66 balance_angel_316
    "leandromoreira53._colorful_vivid_balance_angel_in_gold_and_cr_316bb9d0-debe-411c-83c0-6e236cdcfa9d_2.png",
    # Q67 Ancient_of_Days_1
    "leandromoreira53._colorful_vivid_Ancient_of_Days_in_snow-whit_766b4ce4-61fc-468e-8eb8-420476977e72_1.png",
    # Q68 young_prophet_Daniel_2
    "leandromoreira53._colorful_vivid_young_prophet_Daniel_in_lapi_8ede65f7-a866-4edf-9880-210cb4c10fb3_2.png",
    # Q69 ancient_high_priest_1
    "leandromoreira53._colorful_vivid_ancient_high_priest_in_ivory_c104090d-1c4c-427d-8273-4203f02574f3_1.png",
    # Q70 intercessor_angel_1
    "leandromoreira53._colorful_vivid_intercessor_angel_in_vivid_r_3c81cd50-5f8d-4f6e-9a1d-b91060e935da_1.png",
    # Q71 Babylonian_demon_1
    "leandromoreira53._colorful_vivid_Babylonian_demon_with_black__4942abcc-2274-450b-812f-f5077875758d_1.png",
    # Q72 King_Nebuchadnezzar_0
    "leandromoreira53._colorful_vivid_King_Nebuchadnezzar_in_golde_09cd6aff-98b6-4990-a2a1-17aaabc92e3b_0.png",

    # --- PARTE 5 (Quadros 73-90) — Quadro comparativo + conclusao ---
    # Q73 covenant_angel_0
    "leandromoreira53._colorful_vivid_covenant_angel_in_royal_blue_c8fcb52c-563e-4b9d-bf87-ad215b801f2d_0.png",
    # Q74 Hiram_of_Tyre_1
    "leandromoreira53._colorful_vivid_Hiram_of_Tyre_in_ochre_and_b_d3b05477-3001-4bd7-aaa6-8f99d32b77cb_1.png",
    # Q75 seven-headed_Beast_1
    "leandromoreira53._colorful_vivid_seven-headed_Beast_in_blood-_bef16b8b-19e6-4fe7-b5a6-ba03e3fb7c26_1.png",
    # Q76 Archangel_Gabriel_descending_1
    "leandromoreira53._colorful_vivid_Archangel_Gabriel_descending_e01f0017-cfba-4843-9bf0-41fc635c16b6_1.png",
    # Q77 patriarch_Abraham_0
    "leandromoreira53._colorful_vivid_patriarch_Abraham_in_bronze__645e587e-a2d9-4837-a624-534d6aec8979_0.png",
    # Q78 cartographer_angel_1
    "leandromoreira53._colorful_vivid_cartographer_angel_in_purple_dbcd5a0a-355b-4bdf-9fa5-c41a10a6e14f_1.png",
    # Q79 resurrected_Christ_0
    "leandromoreira53._colorful_vivid_resurrected_Christ_in_radian_6b00b688-8a98-4a4c-94ab-ca11f7c6b7ab_0.png",
    # Q80 judgment_angel_0
    "leandromoreira53._colorful_vivid_judgment_angel_with_raised_g_6942d338-ccd7-4915-b37b-0da0a4e7da60_0.png",
    # Q81 mediator_angel_2
    "leandromoreira53._colorful_vivid_mediator_angel_in_white_and__08eed132-fa2a-45df-8959-82d6534cbce0_2.png",
    # Q82 King_Solomon_tribute_1
    "leandromoreira53._colorful_vivid_King_Solomon_receiving_tribu_06e2a2d5-5c14-499a-9778-e9849fa13254_1.png",
    # Q83 King_Solomon_tribute_0
    "leandromoreira53._colorful_vivid_King_Solomon_receiving_tribu_06e2a2d5-5c14-499a-9778-e9849fa13254_0.png",
    # Q84 oracle_white_amber_0
    "leandromoreira53._colorful_vivid_oracle_in_white_and_amber_ro_cc39c66c-f11d-4dfa-80d4-9670a9a7cc20_0.png",
    # Q85 oracle_white_amber_1
    "leandromoreira53._colorful_vivid_oracle_in_white_and_amber_ro_cc39c66c-f11d-4dfa-80d4-9670a9a7cc20_1.png",
    # Q86 shadow_angel_0
    "leandromoreira53._colorful_vivid_shadow_angel_in_jet-black_an_8d659418-f978-48f2-b477-e89c9debad02_0.png",
    # Q87 apocalyptic_prophetess_2
    "leandromoreira53._colorful_vivid_apocalyptic_prophetess_in_sc_a19f05a5-c3ba-4a50-841b-6c85d3f41069_2.png",
    # Q88 accountant_angel_1
    "leandromoreira53._colorful_vivid_accountant_angel_in_sapphire_14c1a569-8589-43eb-9763-3ad301193d8d_1.png",
    # Q89 modern_Prometheus_1
    "leandromoreira53._colorful_vivid_modern_Prometheus_in_incande_4b539ce8-9bcf-4f7e-8987-d6d34f2621c7_1.png",
    # Q90 hooded_figure_1 (encerramento — volta ao misterio da abertura)
    "leandromoreira53._colorful_vivid_hooded_figure_in_deep_crimso_1d4b066b-2e84-432a-bd11-979521293579_1.png",
]

# Duracao de cada quadro (segundos) — 18 quadros por parte
# Parte 1:  2m10s = 130s / 18 quadros ~ 7.2s por quadro
# Parte 2:  2m20s = 140s / 18 quadros ~ 7.8s
# Parte 3:  2m15s = 135s / 18 quadros ~ 7.5s
# Parte 4:  2m40s = 160s / 18 quadros ~ 8.9s  (4.1 + 4.2 combinados)
# Parte 5:  2m45s = 165s / 18 quadros ~ 9.2s  (5.1 + 5.2 combinados)

DURATIONS_PER_PART = {
    0: 7.2,   # Parte 1 (indices 0-17)
    1: 7.8,   # Parte 2 (indices 18-35)
    2: 7.5,   # Parte 3 (indices 36-53)
    3: 8.9,   # Parte 4 (indices 54-71)
    4: 9.2,   # Parte 5 (indices 72-89)
}

# Ken Burns — direcoes ciclicas para evitar repeticao visual consecutiva
KB_DIRECTIONS = [
    "zoom_in",
    "pan_left",
    "zoom_in",
    "zoom_in_extreme",
    "pan_right",
    "zoom_out",
    "pan_left",
    "zoom_in",
    "pan_right",
    "zoom_out",
    "zoom_in",
    "pan_left",
    "zoom_in",
    "zoom_out",
    "pan_right",
    "zoom_in",
    "zoom_in",
    "zoom_out",
] * 5  # repete o padrao para as 5 partes (90 quadros)


# Arquivos de audio por parte
AUDIO_FILES = [
    "PARTE1.mp3",
    "PARTE2.mp3",
    "PARTE3.mp3",
    "PARTE4_1.mp3",   # 4.1 Musk
    "PARTE4_2.mp3",   # 4.2 Macron (continua na parte 4)
    "PARTE5_1.mp3",   # 5.1 Quadro comparativo
    "PARTE5.2.mp3",   # 5.2 Conclusao
]

# Blocos de quadros correspondentes a cada arquivo de audio
# Mapeamento: arquivo de audio -> (indice_inicio, indice_fim) inclusive
AUDIO_FRAME_MAP = [
    (0,  17),   # PARTE1.mp3       -> quadros 1-18
    (18, 35),   # PARTE2.mp3       -> quadros 19-36
    (36, 53),   # PARTE3.mp3       -> quadros 37-54
    (54, 62),   # PARTE4_1.mp3     -> quadros 55-63 (Musk — ~9 quadros)
    (63, 71),   # PARTE4_2.mp3     -> quadros 64-72 (Macron — ~9 quadros)
    (72, 80),   # PARTE5_1.mp3     -> quadros 73-81 (comparativo — ~9)
    (81, 89),   # PARTE5.2.mp3     -> quadros 82-90 (conclusao — ~9)
]


# ==============================================================================
# FUNCOES DE EFEITO
# ==============================================================================

def ken_burns(clip, zoom_ratio=0.15, direction="zoom_in"):
    """
    Aplica efeito Ken Burns em um ImageClip.
    direction: "zoom_in", "zoom_out", "pan_left", "pan_right", "zoom_in_extreme"
    """
    w, h = clip.size
    duration = clip.duration

    if direction == "zoom_in":
        def make_frame(t):
            progress = t / duration
            scale = 1.0 + zoom_ratio * progress
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_start = (new_w - w) // 2
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_start:x_start+w]

    elif direction == "zoom_out":
        def make_frame(t):
            progress = t / duration
            scale = (1.0 + zoom_ratio) - zoom_ratio * progress
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_start = (new_w - w) // 2
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_start:x_start+w]

    elif direction == "zoom_in_extreme":
        zoom_r = zoom_ratio * 1.5
        def make_frame(t):
            progress = t / duration
            scale = 1.0 + zoom_r * progress
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_start = (new_w - w) // 2
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_start:x_start+w]

    elif direction == "pan_left":
        def make_frame(t):
            progress = t / duration
            scale = 1.0 + zoom_ratio * 0.5
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_offset = int((new_w - w) * progress)
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_offset:x_offset+w]

    elif direction == "pan_right":
        def make_frame(t):
            progress = t / duration
            scale = 1.0 + zoom_ratio * 0.5
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_offset = int((new_w - w) * (1.0 - progress))
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_offset:x_offset+w]

    else:
        # fallback: zoom_in
        def make_frame(t):
            progress = t / duration
            scale = 1.0 + zoom_ratio * progress
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = clip.get_frame(t)
            import cv2
            resized = cv2.resize(img, (new_w, new_h))
            x_start = (new_w - w) // 2
            y_start = (new_h - h) // 2
            return resized[y_start:y_start+h, x_start:x_start+w]

    from moviepy.editor import VideoClip
    return VideoClip(make_frame, duration=duration).set_fps(FPS)


def color_grade(clip):
    """
    Aplica color grading dark via LUT (lookup table).
    Zero alocacao de array grande — so indexacao de 256 valores pre-calculados.
    """
    # Pre-calcular LUT para todos os 256 valores possiveis
    idx = np.arange(256, dtype=np.float32)
    base = np.clip((idx - 128) * CONTRAST_FACTOR * BRIGHTNESS_FACTOR + 128 * BRIGHTNESS_FACTOR, 0, 255).astype(np.uint8)
    lut_r = np.clip(base.astype(np.float32) * 0.98, 0, 255).astype(np.uint8)
    lut_g = base
    lut_b = np.clip(base.astype(np.float32) * 1.01, 0, 255).astype(np.uint8)

    def grade_frame(frame):
        result = np.empty_like(frame)
        result[:, :, 0] = lut_r[frame[:, :, 0]]
        result[:, :, 1] = lut_g[frame[:, :, 1]]
        result[:, :, 2] = lut_b[frame[:, :, 2]]
        return result

    return clip.fl_image(grade_frame)


def vignette(clip):
    """
    Aplica vinheta oval suave nas bordas.
    Usa uma mascara gaussiana invertida aplicada por frame.
    """
    w, h = clip.size
    # Gerar mascara de vinheta (calculada uma vez, aplicada a todos os frames)
    Y, X = np.ogrid[:h, :w]
    cx, cy = w / 2.0, h / 2.0
    # Normalizacao eliptica
    dist = np.sqrt(((X - cx) / (w * 0.55)) ** 2 + ((Y - cy) / (h * 0.55)) ** 2)
    # Mascara: 1.0 no centro, 0.0 nas bordas
    mask = np.clip(1.0 - dist * VIGNETTE_STRENGTH, 0.0, 1.0)
    mask_3ch = np.stack([mask, mask, mask], axis=-1).astype(np.float32)

    def apply_vignette(frame):
        f = frame.astype(np.float32) / 255.0
        f = f * mask_3ch
        return np.clip(f * 255, 0, 255).astype(np.uint8)

    return clip.fl_image(apply_vignette)


def apply_all_fx(clip, kb_direction="zoom_in"):
    """Aplica Ken Burns + color grade + vinheta em sequencia."""
    clip = ken_burns(clip, zoom_ratio=0.15, direction=kb_direction)
    clip = color_grade(clip)
    clip = vignette(clip)
    return clip


# ==============================================================================
# CARREGAMENTO DE IMAGENS E CONSTRUCAO DOS CLIPS
# ==============================================================================

def get_image_path(filename):
    """Resolve caminho absoluto da imagem, com fallback ciclico."""
    path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(path):
        return path
    # Fallback: usar qualquer .png disponivel ciclicamente
    all_pngs = sorted(glob.glob(os.path.join(IMAGES_DIR, "*.png")))
    if not all_pngs:
        raise FileNotFoundError(f"Nenhuma imagem .png encontrada em {IMAGES_DIR}")
    idx = IMAGE_FILENAMES.index(filename) % len(all_pngs)
    print(f"[WARN] Imagem nao encontrada: {filename} — usando fallback: {all_pngs[idx]}")
    return all_pngs[idx]


def build_image_clips():
    """
    Constroi a lista de clips de imagem com Ken Burns aplicado.
    Cada clip tem duracao configurada por parte + tempo de crossfade
    para que o crossfade nao corte o conteudo real.
    """
    clips = []
    total = len(IMAGE_FILENAMES)

    for idx, filename in enumerate(IMAGE_FILENAMES):
        part_idx = idx // 18
        base_dur = DURATIONS_PER_PART.get(part_idx, 7.0)
        # Adiciona metade do crossfade em cada extremidade para suavizar a transicao
        duration = base_dur + CROSSFADE

        img_path = get_image_path(filename)
        direction = KB_DIRECTIONS[idx % len(KB_DIRECTIONS)]

        print(f"[{idx+1:02d}/{total}] Carregando: {os.path.basename(img_path)} | {direction} | {duration:.1f}s")

        # Carrega imagem, redimensiona para 1920x1080 mantendo o crop
        clip = (
            ImageClip(img_path)
            .resize(RESOLUTION)
            .set_duration(duration)
        )

        # Aplica todos os efeitos cinematograficos
        clip = apply_all_fx(clip, kb_direction=direction)

        clips.append(clip)

    return clips


# ==============================================================================
# CARREGAMENTO DE AUDIO E SINCRONIZACAO
# ==============================================================================

def load_audio_tracks():
    """Carrega todos os arquivos MP3 e concatena na ordem correta."""
    audio_clips = []
    for audio_file in AUDIO_FILES:
        path = os.path.join(AUDIO_DIR, audio_file)
        if os.path.exists(path):
            print(f"[AUDIO] Carregando: {audio_file}")
            audio_clips.append(AudioFileClip(path))
        else:
            print(f"[WARN] Audio nao encontrado: {audio_file}")

    if not audio_clips:
        raise FileNotFoundError("Nenhum arquivo de audio encontrado.")

    return concatenate_audioclips(audio_clips)


def sync_audio_to_video(video_clip, audio_clip):
    """
    Sincroniza audio ao video.
    Se o video for mais longo que o audio, o audio termina e o video continua mudo.
    Se o audio for mais longo, trunca o video para o tamanho do audio.
    """
    video_dur = video_clip.duration
    audio_dur = audio_clip.duration

    print(f"[SYNC] Video: {video_dur:.1f}s | Audio: {audio_dur:.1f}s")

    if audio_dur > video_dur:
        print(f"[SYNC] Audio mais longo — ultimo quadro sera estendido.")
        # Extende o ultimo frame ate o audio terminar
        # Ja esta coberto pela logica de duracao dos clips

    return video_clip.set_audio(audio_clip)


# ==============================================================================
# CROSSFADE E MONTAGEM FINAL
# ==============================================================================

def build_final_video(image_clips):
    """
    Monta o video final com crossfade entre clips.
    Usa CompositeVideoClip com offsets temporais para sobreposicao suave.
    """
    print(f"\n[MONTAGEM] Concatenando {len(image_clips)} clips com crossfade de {CROSSFADE}s...")

    clips_with_fade = []
    start_time = 0.0

    for i, clip in enumerate(image_clips):
        # Aplica fade in/out para crossfade suave
        if i == 0:
            faded = clip.crossfadeout(CROSSFADE)
        elif i == len(image_clips) - 1:
            faded = clip.crossfadein(CROSSFADE)
        else:
            faded = clip.crossfadein(CROSSFADE).crossfadeout(CROSSFADE)

        faded = faded.set_start(start_time)
        clips_with_fade.append(faded)

        # Proximo clip inicia CROSSFADE segundos antes do fim deste
        start_time += clip.duration - CROSSFADE

    # Composita todos os clips com sobreposicao temporal
    final = CompositeVideoClip(clips_with_fade, size=RESOLUTION)
    return final


# ==============================================================================
# EXPORT
# ==============================================================================

def export_video(final_clip):
    """Exporta o video final em H.264/AAC."""
    output_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[EXPORT] Renderizando: {OUTPUT_PATH}")
    print(f"[EXPORT] Resolucao: {RESOLUTION[0]}x{RESOLUTION[1]} | FPS: {FPS}")
    print(f"[EXPORT] Duracao estimada: {final_clip.duration:.1f}s")

    final_clip.write_videofile(
        OUTPUT_PATH,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",        # balance entre velocidade e qualidade
        bitrate="8000k",        # 8 Mbps para 1080p de alta qualidade
        audio_bitrate="192k",
        threads=4,
        temp_audiofile="temp_audio_video009.m4a",
        remove_temp=True,
        verbose=False,
        logger="bar",
    )
    print(f"\n[OK] Video exportado com sucesso: {OUTPUT_PATH}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 60)
    print("PHANTASMA — video-009-anticristo — Montagem v1")
    print("Abismo Criativo | Canal: Sinais do Fim")
    print("=" * 60)

    # 1. Construir clips de imagem
    print(f"\n[FASE 1] Construindo {len(IMAGE_FILENAMES)} clips de imagem...")
    image_clips = build_image_clips()

    # 2. Montar video com crossfade
    print("\n[FASE 2] Montando video com crossfade...")
    video_clip = build_final_video(image_clips)

    # 3. Carregar audio
    print("\n[FASE 3] Carregando trilha de audio...")
    audio_clip = load_audio_tracks()

    # 4. Sincronizar audio + video
    print("\n[FASE 4] Sincronizando audio...")
    final_clip = sync_audio_to_video(video_clip, audio_clip)

    # 5. Exportar
    print("\n[FASE 5] Exportando MP4...")
    export_video(final_clip)

    # 6. Limpeza
    video_clip.close()
    audio_clip.close()
    final_clip.close()
    for c in image_clips:
        c.close()

    print("\n[PHANTASMA] Montagem concluida.")


if __name__ == "__main__":
    main()
