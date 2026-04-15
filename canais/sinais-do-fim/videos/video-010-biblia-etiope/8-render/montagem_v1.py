# video-010-biblia-etiope — Phantasma MoviePy Script
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

OUTPUT_PATH = "canais/sinais-do-fim/videos/video-010-biblia-etiope/8-render/video-010-biblia-etiope_v1.mp4"
IMAGES_DIR  = "canais/sinais-do-fim/videos/video-010-biblia-etiope/7-imagens/"
AUDIO_DIR   = "canais/sinais-do-fim/videos/video-010-biblia-etiope/5-audio/"
FPS         = 24
RESOLUTION  = (1920, 1080)
CROSSFADE   = 0.5   # segundos de crossfade entre clips

# Cores do canal (paleta dark)
VIGNETTE_STRENGTH = 0.55   # 0.0 = sem vinheta, 1.0 = borda totalmente preta
BRIGHTNESS_FACTOR = 0.90   # 0.90 = -10% de brilho
CONTRAST_FACTOR   = 1.15   # 1.15 = +15% de contraste

# ==============================================================================
# MAPEAMENTO DE IMAGENS — 91 quadros, 13 por parte (7 partes)
# ==============================================================================

IMAGE_FILENAMES = [
    # --- PARTE 1 (Quadros 1-13) — GANCHO: A Biblia Proibida ---
    "leandromoreira53._colorful_vivid_ancient_Ethiopian_prophet_el_1fe90d92-1975-4ffc-83b2-522a7e7ce7c3_0.png",
    "leandromoreira53._colorful_vivid_ancient_Geez_manuscript_parc_57fbc94c-f6d6-4425-a838-8eeab034a91c_1.png",
    "leandromoreira53._colorful_vivid_Ethiopian_mountain_monastery_789c5b49-447b-4df2-bcca-0707eb86f429_2.png",
    "leandromoreira53._colorful_vivid_aerial_diagonal_view_of_Ethi_d0464893-899f-4012-b2a0-084341bb188b_0.png",
    "leandromoreira53._colorful_vivid_Ethiopian_Bible_close-up_woo_128b5d8e-0aa6-43d0-a349-3e69f89422e7_1.png",
    "leandromoreira53._colorful_vivid_Ethiopian_illuminated_manusc_aefd3fad-6e51-4f6a-82e9-46a614056840_1.png",
    "leandromoreira53._colorful_vivid_dramatic_extreme_close-up_po_b91e34ef-63c1-4ff9-8b74-019cf4f375df_0.png",
    "leandromoreira53._colorful_vivid_extreme_close-up_of_aged_dar_32a933ae-a6c7-4a34-a5e5-bf0fb3d4adb0_0.png",
    "leandromoreira53._colorful_vivid_group_of_medieval_European_b_43b29eae-a00d-47a2-a14d-2d382fd3bda5_1.png",
    "leandromoreira53._olorful_vivid_two_ancient_manuscripts_open__2fe1e0e3-249a-4f50-8b18-b947b9979fb1_1.png",
    "leandromoreira53._colorful_vivid_abstract_overlay_of_two_anci_1d1ed5a4-ceb4-4713-a576-373af1238372_0.png",
    "leandromoreira53._colorful_vivid_Ethiopian_stone_monastery_at_ea0a6163-56bb-43a6-b4c0-f254b7df23bf_1.png",
    "leandromoreira53._colorful_vivid_ancient_Ethiopian_prophet_el_1fe90d92-1975-4ffc-83b2-522a7e7ce7c3_3.png",

    # --- PARTE 2 (Quadros 14-26) — Os 22 Livros Ocultos ---
    "leandromoreira53._colorful_vivid_Enoch_the_prophet_as_ancient_da90e7a9-6a89-4f30-b005-20c21f1ab4fb_2.png",
    "leandromoreira53._colorful_vivid_open_Book_of_Enoch_with_hand_1e6befc5-b248-48ba-a96b-11c1f596145e_1.png",
    "leandromoreira53._colorful_vivid_epic_wide_shot_of_the_Watche_c7c88001-8f91-4422-a8d4-3a7aa5ee18ba_3.png",
    "leandromoreira53._colorful_vivid_fallen_angels_as_falling_sta_8836d318-695b-4bf0-aba0-d32394b11c0c_1.png",
    "leandromoreira53._colorful_vivid_Nephilim_giant_on_ancient_ba_9b8db744-5b29-48a9-a6cb-11d2ec6e49b0_2.png",
    "leandromoreira53._colorful_vivid_fallen_angel_Azazel_with_tor_1e437345-7ee2-4dbb-82df-5cd4ce202ca7_2.png",
    "leandromoreira53._colorful_vivid_Noah_in_crimson_and_gold_rob_bada8441-1d9b-4484-b858-aaea00d2105d_1.png",
    "leandromoreira53._colorful_vivid_abstract_depiction_of_Nephil_9a45629c-ef53-43b6-8678-5d80570ff32e_0.png",
    "leandromoreira53._colorful_vivid_burning_volcanic_mountain_in_7839c033-2f42-44e4-9ef6-a177a166caec_1.png",
    "leandromoreira53._colorful_vivid_open_Book_of_Enoch_with_hand_1e6befc5-b248-48ba-a96b-11c1f596145e_2.png",
    "leandromoreira53._colorful_vivid_Enoch_enthroned_in_celestial_19c10f0d-5c76-4d16-b37b-b8a21f65fafa_1.png",
    "leandromoreira53._colorful_vivid_fallen_angels_as_falling_sta_8836d318-695b-4bf0-aba0-d32394b11c0c_2.png",
    "leandromoreira53._colorful_vivid_Nephilim_giant_on_ancient_ba_9b8db744-5b29-48a9-a6cb-11d2ec6e49b0_3.png",

    # --- PARTE 3 (Quadros 27-39) — O Concilio que Censurou ---
    "leandromoreira53._colorful_vivid_Council_of_Laodicea_bishops__e84082fa-0d9c-4435-aaa0-8ca5f9878207_0.png",
    "leandromoreira53._colorful_vivid_group_of_medieval_European_b_43b29eae-a00d-47a2-a14d-2d382fd3bda5_2.png",
    "leandromoreira53._colorful_vivid_nocturnal_tribunal_scene_by__914967b9-2436-42c9-a62e-ec090021ba09_1.png",
    "leandromoreira53._colorful_vivid_extreme_close-up_of_broken_c_5173e3ba-7ef5-46ff-8ea3-9ca1aeddf908_2.png",
    "leandromoreira53._colorful_vivid_Constantinople_in_flames_fro_5a35295f-39e9-4356-82a9-a746222a40b6_1.png",
    "leandromoreira53._colorful_vivid_Council_of_Laodicea_bishops__e84082fa-0d9c-4435-aaa0-8ca5f9878207_1.png",
    "leandromoreira53._colorful_vivid_medieval_illuminated_Apocaly_4a7261ed-5ad3-49ea-a0ed-0273f1239e18_2.png",
    "leandromoreira53._colorful_vivid_large-scale_film_set_in_full_3ca9cae7-ef96-46a2-bc92-20785336decf_1.png",
    "leandromoreira53._colorful_vivid_Scottish_18th_century_explor_4214d673-ec3b-45b0-9f2f-704ece4dd96f_3.png",
    "leandromoreira53._colorful_vivid_Council_of_Laodicea_bishops__e84082fa-0d9c-4435-aaa0-8ca5f9878207_2.png",
    "leandromoreira53._colorful_vivid_Constantinople_in_flames_fro_5a35295f-39e9-4356-82a9-a746222a40b6_2.png",
    "leandromoreira53._colorful_vivid_nocturnal_tribunal_scene_by__914967b9-2436-42c9-a62e-ec090021ba09_3.png",
    "leandromoreira53._colorful_vivid_Council_of_Laodicea_bishops__e84082fa-0d9c-4435-aaa0-8ca5f9878207_3.png",

    # --- PARTE 4 (Quadros 40-52) — Os Manuscritos do Mar Morto ---
    "leandromoreira53._colorful_vivid_aerial_view_of_Qumran_ruins__6ae0b2dd-37b3-46fb-b49d-ef41e341a33e_1.png",
    "leandromoreira53._colorful_vivid_Qumran_clay_jar_in_extreme_c_cc3fdcb0-382e-42f8-9792-3736ff28dac6_2.png",
    "leandromoreira53._colorful_vivid_aerial_view_of_Qumran_ruins__6ae0b2dd-37b3-46fb-b49d-ef41e341a33e_2.png",
    "leandromoreira53._colorful_vivid_open_Book_of_Enoch_with_hand_1e6befc5-b248-48ba-a96b-11c1f596145e_3.png",
    "leandromoreira53._colorful_vivid_archangel_Uriel_in_ultramari_153cfe7e-4a3c-41fb-bad1-2d865b6e9d6f_1.png",
    "leandromoreira53._colorful_vivid_celestial_judgment_tablets_f_9fb88d8d-7443-4f96-ad3b-0c5aaebb3215_1.png",
    "leandromoreira53._colorful_vivid_extreme_close-up_of_chained__ef07ba85-5b3b-4c76-bf01-cea4f1023a9e_0.png",
    "leandromoreira53._colorful_vivid_seven_medieval_archangels_in_b1e68fed-257b-472a-a660-c613a0fc12d6_1.png",
    "leandromoreira53._colorful_vivid_burning_volcanic_mountain_in_7839c033-2f42-44e4-9ef6-a177a166caec_2.png",
    "leandromoreira53._colorful_vivid_archangel_Uriel_in_ultramari_153cfe7e-4a3c-41fb-bad1-2d865b6e9d6f_3.png",
    "leandromoreira53._colorful_vivid_celestial_judgment_tablets_f_9fb88d8d-7443-4f96-ad3b-0c5aaebb3215_3.png",
    "leandromoreira53._colorful_vivid_extreme_close-up_of_chained__ef07ba85-5b3b-4c76-bf01-cea4f1023a9e_3.png",
    "leandromoreira53._colorful_vivid_Enoch_enthroned_in_celestial_19c10f0d-5c76-4d16-b37b-b8a21f65fafa_2.png",

    # --- PARTE 4_1 (Quadros 53-65) — Os Livros Apocrifos ---
    "leandromoreira53._colorful_vivid_apostle_Jude_in_emerald_gree_e9d5232e-7ad2-4c73-81f6-57aa79751b73_1.png",
    "leandromoreira53._colorful_vivid_Gospel_of_Nicodemus_illumina_43559009-5d26-4942-9394-b8dfa63238e8_1.png",
    "leandromoreira53._colorful_vivid_Harrowing_of_Hell_scene_Jesu_5cf21b35-0ffb-4300-aba0-ee9d8fad170d_1.png",
    "leandromoreira53._colorful_vivid_apostle_Jude_in_emerald_gree_e9d5232e-7ad2-4c73-81f6-57aa79751b73_2.png",
    "leandromoreira53._colorful_vivid_Gospel_of_Nicodemus_illumina_43559009-5d26-4942-9394-b8dfa63238e8_2.png",
    "leandromoreira53._colorful_vivid_Harrowing_of_Hell_scene_Jesu_5cf21b35-0ffb-4300-aba0-ee9d8fad170d_3.png",
    "leandromoreira53._colorful_vivid_powerful_close-up_of_two_han_f9f56755-9993-469f-ae3a-56df1448410c_1.png",
    "leandromoreira53._colorful_vivid_seven_medieval_archangels_in_b1e68fed-257b-472a-a660-c613a0fc12d6_2.png",
    "leandromoreira53._colorful_vivid_abstract_overlay_of_two_anci_1d1ed5a4-ceb4-4713-a576-373af1238372_3.png",
    "leandromoreira53._colorful_vivid_medieval_illuminated_Apocaly_4a7261ed-5ad3-49ea-a0ed-0273f1239e18_3.png",
    "leandromoreira53._colorful_vivid_seven_medieval_archangels_in_b1e68fed-257b-472a-a660-c613a0fc12d6_3.png",
    "leandromoreira53._olorful_vivid_two_ancient_manuscripts_open__2fe1e0e3-249a-4f50-8b18-b947b9979fb1_2.png",
    "leandromoreira53._colorful_vivid_dramatic_extreme_close-up_po_b91e34ef-63c1-4ff9-8b74-019cf4f375df_3.png",

    # --- PARTE 5 (Quadros 66-78) — O Apocalipse e o Juizo Final ---
    "leandromoreira53._colorful_vivid_John_of_Patmos_in_blood-red__fa6e5da7-a1bb-4d94-864e-68aa6ded0a41_3.png",
    "leandromoreira53._colorful_vivid_island_of_Patmos_at_sunset_r_42980e7c-e35b-45d0-b0c0-1b49ab0f9a51_0.png",
    "leandromoreira53._colorful_vivid_Book_of_Revelation_open_on_o_90b9e481-b67c-4850-b7ef-8e9b7c5f15dc_0.png",
    "leandromoreira53._colorful_vivid_Beast_of_Revelation_emerging_daf26660-965b-4117-a85a-8a4a87d52c51_1.png",
    "leandromoreira53._colorful_vivid_subjective_upward_view_from__cf84602d-5bad-4d86-af09-80e1359ed94a_2.png",
    "leandromoreira53._colorful_vivid_aerial_night_view_of_Saint_P_7e39b29e-830e-4e18-bd8a-03766776516b_0.png",
    "leandromoreira53._colorful_vivid_Book_of_Revelation_open_on_o_90b9e481-b67c-4850-b7ef-8e9b7c5f15dc_2.png",
    "leandromoreira53._colorful_vivid_Beast_of_Revelation_emerging_daf26660-965b-4117-a85a-8a4a87d52c51_3.png",
    "leandromoreira53._colorful_vivid_island_of_Patmos_at_sunset_r_42980e7c-e35b-45d0-b0c0-1b49ab0f9a51_3.png",
    "leandromoreira53._colorful_vivid_subjective_upward_view_from__cf84602d-5bad-4d86-af09-80e1359ed94a_3.png",
    "leandromoreira53._colorful_vivid_Book_of_Revelation_open_on_o_90b9e481-b67c-4850-b7ef-8e9b7c5f15dc_3.png",
    "leandromoreira53._colorful_vivid_aerial_night_view_of_Saint_P_a7f474cf-2e69-4aed-aae3-3b8c4f1a0d8b_3.png",
    "leandromoreira53._colorful_vivid_subjective_perspective_from__5493e623-7c15-4298-87d5-7b8e80af9d94_3.png",

    # --- PARTE 6 (Quadros 79-91) — Encerramento: A Verdade Oculta ---
    "leandromoreira53._colorful_vivid_extreme_close-up_of_aged_dar_32a933ae-a6c7-4a34-a5e5-bf0fb3d4adb0_2.png",
    "leandromoreira53._colorful_vivid_aerial_diagonal_view_of_Ethi_d0464893-899f-4012-b2a0-084341bb188b_1.png",
    "leandromoreira53._colorful_vivid_subjective_first-person_pers_c01b177a-c1b0-49c1-b49c-206d8a7132ff_1.png",
    "leandromoreira53._colorful_vivid_upward_subjective_perspectiv_fc6f662b-c6bc-4800-b766-dcdb3922fa0c_3.png",
    "leandromoreira53._colorful_vivid_Ethiopian_stone_monastery_at_ea0a6163-56bb-43a6-b4c0-f254b7df23bf_2.png",
    "leandromoreira53._colorful_vivid_extreme_close-up_of_aged_dar_32a933ae-a6c7-4a34-a5e5-bf0fb3d4adb0_3.png",
    "leandromoreira53._colorful_vivid_aerial_diagonal_view_of_Ethi_d0464893-899f-4012-b2a0-084341bb188b_3.png",
    "leandromoreira53._colorful_vivid_subjective_first-person_pers_c01b177a-c1b0-49c1-b49c-206d8a7132ff_2.png",
    "leandromoreira53._colorful_vivid_ancient_Geez_manuscript_parc_57fbc94c-f6d6-4425-a838-8eeab034a91c_2.png",
    "leandromoreira53._colorful_vivid_Ethiopian_illuminated_manusc_aefd3fad-6e51-4f6a-82e9-46a614056840_3.png",
    "leandromoreira53._colorful_vivid_Ethiopian_Bible_close-up_woo_128b5d8e-0aa6-43d0-a349-3e69f89422e7_2.png",
    "leandromoreira53._colorful_vivid_wide_final_shot_of_Ethiopian_9ba67fed-1b2a-4f46-be0d-f813e16d7851_2.png",
    "leandromoreira53._colorful_vivid_ancient_Ethiopian_prophet_el_1fe90d92-1975-4ffc-83b2-522a7e7ce7c3_0.png",
]

# Duracao base por parte (segundos por imagem)
# 91 imagens / 7 partes = 13 imagens por parte
DURATIONS_PER_PART = {
    0: 8.0,   # Parte 1 — indices 0-12
    1: 8.5,   # Parte 2 — indices 13-25
    2: 8.5,   # Parte 3 — indices 26-38
    3: 9.0,   # Parte 4 — indices 39-51
    4: 9.0,   # Parte 4_1 — indices 52-64
    5: 9.5,   # Parte 5 — indices 65-77
    6: 9.5,   # Parte 6 — indices 78-90
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
    "zoom_out",
] * 7  # repete o padrao para as 7 partes (91 quadros)

# Arquivos de audio por parte
AUDIO_FILES = [
    "PARTE1.mp3",
    "PARTE2.mp3",
    "PARTE3.mp3",
    "PARTE4.mp3",
    "PARTE4_1.mp3",
    "PARTE5.mp3",
    "PARTE6.mp3",
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
    """Aplica vinheta oval suave nas bordas."""
    w, h = clip.size
    Y, X = np.ogrid[:h, :w]
    cx, cy = w / 2.0, h / 2.0
    dist = np.sqrt(((X - cx) / (w * 0.55)) ** 2 + ((Y - cy) / (h * 0.55)) ** 2).astype(np.float32)
    mask = np.clip(np.float32(1.0) - dist * np.float32(VIGNETTE_STRENGTH), np.float32(0.0), np.float32(1.0))
    mask_3ch = np.stack([mask, mask, mask], axis=-1)

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
    all_pngs = sorted(glob.glob(os.path.join(IMAGES_DIR, "*.png")))
    if not all_pngs:
        raise FileNotFoundError(f"Nenhuma imagem .png encontrada em {IMAGES_DIR}")
    idx = IMAGE_FILENAMES.index(filename) % len(all_pngs)
    print(f"[WARN] Imagem nao encontrada: {filename} — usando fallback: {all_pngs[idx]}")
    return all_pngs[idx]


def build_image_clips():
    """Constroi a lista de clips de imagem com Ken Burns aplicado."""
    clips = []
    total = len(IMAGE_FILENAMES)

    for idx, filename in enumerate(IMAGE_FILENAMES):
        part_idx = idx // 13   # 13 imagens por parte
        base_dur = DURATIONS_PER_PART.get(part_idx, 8.5)
        duration = base_dur + CROSSFADE

        img_path = get_image_path(filename)
        direction = KB_DIRECTIONS[idx % len(KB_DIRECTIONS)]

        print(f"[{idx+1:02d}/{total}] Carregando: {os.path.basename(img_path)} | {direction} | {duration:.1f}s")

        clip = (
            ImageClip(img_path)
            .resize(RESOLUTION)
            .set_duration(duration)
        )
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
    """Sincroniza audio ao video."""
    video_dur = video_clip.duration
    audio_dur = audio_clip.duration
    print(f"[SYNC] Video: {video_dur:.1f}s | Audio: {audio_dur:.1f}s")
    if audio_dur > video_dur:
        print(f"[SYNC] Audio mais longo — ultimo quadro sera estendido.")
    return video_clip.set_audio(audio_clip)


# ==============================================================================
# CROSSFADE E MONTAGEM FINAL
# ==============================================================================

def build_final_video(image_clips):
    """Monta o video final com crossfade entre clips."""
    print(f"\n[MONTAGEM] Concatenando {len(image_clips)} clips com crossfade de {CROSSFADE}s...")

    clips_with_fade = []
    start_time = 0.0

    for i, clip in enumerate(image_clips):
        if i == 0:
            faded = clip.crossfadeout(CROSSFADE)
        elif i == len(image_clips) - 1:
            faded = clip.crossfadein(CROSSFADE)
        else:
            faded = clip.crossfadein(CROSSFADE).crossfadeout(CROSSFADE)

        faded = faded.set_start(start_time)
        clips_with_fade.append(faded)
        start_time += clip.duration - CROSSFADE

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
        preset="medium",
        bitrate="8000k",
        audio_bitrate="192k",
        threads=4,
        temp_audiofile="temp_audio_video010.m4a",
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
    print("PHANTASMA — video-010-biblia-etiope — Montagem v1")
    print("Abismo Criativo | Canal: Sinais do Fim")
    print("=" * 60)

    print(f"\n[FASE 1] Construindo {len(IMAGE_FILENAMES)} clips de imagem...")
    image_clips = build_image_clips()

    print("\n[FASE 2] Montando video com crossfade...")
    video_clip = build_final_video(image_clips)

    print("\n[FASE 3] Carregando trilha de audio...")
    audio_clip = load_audio_tracks()

    print("\n[FASE 4] Sincronizando audio...")
    final_clip = sync_audio_to_video(video_clip, audio_clip)

    print("\n[FASE 5] Exportando MP4...")
    export_video(final_clip)

    video_clip.close()
    audio_clip.close()
    final_clip.close()
    for c in image_clips:
        c.close()

    print("\n[PHANTASMA] Montagem concluida.")


if __name__ == "__main__":
    main()
