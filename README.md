# ppu-paddle-ocr-models

This repository contains models necessarily use by [ppu-paddle-ocr](https://github.com/PT-Perkasa-Pilar-Utama/ppu-paddle-ocr) library.

The models are onnx sourced from https://www.paddleocr.ai/main/en/index.html.

```ts
export const MODEL_BASE_URL =
  "https://media.githubusercontent.com/media/PT-Perkasa-Pilar-Utama/ppu-paddle-ocr-models/main";

export const DICT_BASE_URL =
  "https://raw.githubusercontent.com/PT-Perkasa-Pilar-Utama/ppu-paddle-ocr-models/main";
```

# File tree

```bash
.
├── LICENSE
├── README.md
├── detection
│   ├── PP-OCRv4_mobile_det_infer.onnx
│   ├── PP-OCRv4_server_det_infer.onnx
│   ├── PP-OCRv5_mobile_det_infer.onnx
│   └── PP-OCRv5_server_det_infer.onnx
└── recognition
    ├── PP-OCRv3_mobile_rec_infer.onnx
    ├── PP-OCRv4_mobile_rec_infer.onnx
    ├── PP-OCRv4_server_rec_doc_infer.onnx
    ├── PP-OCRv4_server_rec_infer.onnx
    ├── PP-OCRv5_mobile_rec_infer.onnx
    ├── PP-OCRv5_server_rec_infer.onnx
    ├── multi
    │   ├── arabic
    │   │   └── v5
    │   │       ├── arabic_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_arabic_dict.txt
    │   ├── cyrillic
    │   │   └── v5
    │   │       ├── cyrillic_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_cyrillic_dict.txt
    │   ├── devanagari
    │   │   └── v5
    │   │       ├── devanagari_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_devanagari_dict.txt
    │   ├── el
    │   │   └── v5
    │   │       ├── el_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_el_dict.txt
    │   ├── en
    │   │   ├── v4
    │   │   │   ├── en_PP-OCRv4_mobile_rec_infer.onnx
    │   │   │   └── en_dict.txt
    │   │   └── v5
    │   │       ├── en_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_en_dict.txt
    │   ├── eslav
    │   │   └── v5
    │   │       ├── eslav_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_eslav_dict.txt
    │   ├── japan
    │   │   └── v3
    │   │       ├── japan_PP-OCRv3_mobile_rec_infer.onnx
    │   │       └── japan_dict.txt
    │   ├── korean
    │   │   └── v5
    │   │       ├── korean_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_korean_dict.txt
    │   ├── latin
    │   │   └── v5
    │   │       ├── latin_PP-OCRv5_mobile_rec_infer.onnx
    │   │       └── ppocrv5_latin_dict.txt
    │   ├── ta
    │   │   └── v5
    │   │       ├── ppocrv5_ta_dict.txt
    │   │       └── ta_PP-OCRv5_mobile_rec_infer.onnx
    │   ├── te
    │   │   └── v5
    │   │       ├── ppocrv5_te_dict.txt
    │   │       └── te_PP-OCRv5_mobile_rec_infer.onnx
    │   └── th
    │       └── v5
    │           ├── ppocrv5_th_dict.txt
    │           └── th_PP-OCRv5_mobile_rec_infer.onnx
    ├── ppocrv3_dict.txt
    ├── ppocrv4_dict.txt
    ├── ppocrv4_doc_dict.txt
    └── ppocrv5_dict.txt
```

# Models and Their Supported Languages

| Model                          | Supported Languages                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| korean_PP-OCRv5_mobile_rec     | Korean, English                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| latin_PP-OCRv5_mobile_rec      | French, German, Afrikaans, Italian, Spanish, Bosnian, Portuguese, Czech, Welsh, Danish, Estonian, Irish, Croatian, Uzbek, Hungarian, Serbian (Latin), Indonesian, Occitan, Icelandic, Lithuanian, Maori, Malay, Dutch, Norwegian, Polish, Slovak, Slovenian, Albanian, Swedish, Swahili, Tagalog, Turkish, Latin, Azerbaijani, Kurdish, Latvian, Maltese, Pali, Romanian, Vietnamese, Finnish, Basque, Galician, Luxembourgish, Romansh, Catalan, Quechua |
| eslav_PP-OCRv5_mobile_rec      | Russian, Belarusian, Ukrainian, English                                                                                                                                                                                                                                                                                                                                                                                                                   |
| th_PP-OCRv5_mobile_rec         | Thai, English                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| el_PP-OCRv5_mobile_rec         | Greek, English                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| en_PP-OCRv5_mobile_rec         | English                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| cyrillic_PP-OCRv5_mobile_rec   | Russian, Belarusian, Ukrainian, Serbian (Cyrillic), Bulgarian, Mongolian, Abkhazian, Adyghe, Kabardian, Avar, Dargin, Ingush, Chechen, Lak, Lezgin, Tabasaran, Kazakh, Kyrgyz, Tajik, Macedonian, Tatar, Chuvash, Bashkir, Malian, Moldovan, Udmurt, Komi, Ossetian, Buryat, Kalmyk, Tuvan, Sakha, Karakalpak, English                                                                                                                                    |
| arabic_PP-OCRv5_mobile_rec     | Arabic, Persian, Uyghur, Urdu, Pashto, Kurdish, Sindhi, Balochi, English                                                                                                                                                                                                                                                                                                                                                                                  |
| devanagari_PP-OCRv5_mobile_rec | Hindi, Marathi, Nepali, Bihari, Maithili, Angika, Bhojpuri, Magahi, Santali, Newari, Konkani, Sanskrit, Haryanvi, English                                                                                                                                                                                                                                                                                                                                 |
| ta_PP-OCRv5_mobile_rec         | Tamil, English                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| te_PP-OCRv5_mobile_rec         | Telugu, English                                                                                                                                                                                                                                                                                                                                                                                                                                           |
