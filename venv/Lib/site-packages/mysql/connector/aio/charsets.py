# Copyright (c) 2023, 2024, Oracle and/or its affiliates.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is designed to work with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation. The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have either included with
# the program or referenced in the documentation.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

"""This module contains the MySQL Server Character Sets."""

__all__ = ["Charset", "charsets"]

from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, Optional, Sequence, Tuple

from ..errors import ProgrammingError


@dataclass
class Charset:
    """Dataclass representing a character set."""

    charset_id: int
    name: str
    collation: str
    is_default: bool


class Charsets:
    """MySQL supported character sets and collations class.

    This class holds the list of character sets with their collations supported by
    MySQL, making available methods to get character sets by name, collation, or ID.
    It uses a sparse matrix or tree-like representation using a dict in a dict to hold
    the character set name and collations combinations.
    The list is hardcoded, so we avoid a database query when getting the name of the
    used character set or collation.

    The call of ``charsets.set_mysql_major_version()`` should be done before using any
    of the retrieval methods.

    Usage:
        >>> from mysql.connector.aio.charsets import charsets
        >>> charsets.set_mysql_major_version(8)
        >>> charsets.get_by_name("utf-8")
        Charset(charset_id=255,
                name='utf8mb4',
                collation='utf8mb4_0900_ai_ci',
                is_default=True)
    """

    def __init__(self) -> None:
        self._charset_id_store: Dict[int, Charset] = {}
        self._collation_store: Dict[str, Charset] = {}
        self._name_store: DefaultDict[str, Dict[str, Charset]] = defaultdict(dict)
        self._mysql_major_version: Optional[int] = None

    def set_mysql_major_version(self, version: int) -> None:
        """Set the MySQL major version.

        Sets what tuple should be used based on the MySQL major version to store the
        list of character sets and collations.

        Args:
            version: The MySQL major version (i.e. 8 or 5)
        """
        self._mysql_major_version = version
        self._charset_id_store.clear()
        self._collation_store.clear()
        self._name_store.clear()

        charsets_tuple: Sequence[Tuple[int, str, str, bool]] = None
        if version >= 8:
            charsets_tuple = MYSQL_8_CHARSETS
        elif version == 5:
            charsets_tuple = MYSQL_5_CHARSETS
        else:
            raise ProgrammingError("Invalid MySQL major version")

        for charset_id, name, collation, is_default in charsets_tuple:
            charset = Charset(charset_id, name, collation, is_default)
            self._charset_id_store[charset_id] = charset
            self._collation_store[collation] = charset
            self._name_store[name][collation] = charset

    def get_by_id(self, charset_id: int) -> Charset:
        """Get character set by ID.

        Args:
            charset_id: The charset ID.

        Returns:
            Charset: The Charset dataclass instance.
        """
        try:
            return self._charset_id_store[charset_id]
        except KeyError as err:
            raise ProgrammingError(f"Character set ID {charset_id} unknown") from err

    def get_by_collation(self, collation: str) -> Charset:
        """Get character set by collation.

        Args:
            collation: The collation name.

        Returns:
            Charset: The Charset dataclass instance.
        """
        try:
            return self._collation_store[collation]
        except KeyError as err:
            raise ProgrammingError(f"Collation {collation} unknown") from err

    def get_by_name(self, name: str) -> Charset:
        """Get character set by name.

        Args:
            name: The charset name.

        Returns:
            Charset: The Charset dataclass instance.
        """
        try:
            if name in ("utf8", "utf-8") and self._mysql_major_version == 8:
                name = "utf8mb4"
            for charset in self._name_store[name].values():
                if charset.is_default:
                    return charset
        except KeyError as err:
            raise ProgrammingError(f"Character set name {name} unknown") from err
        raise ProgrammingError(f"No default was found for character set '{name}'")

    def get_by_name_and_collation(self, name: str, collation: str) -> Charset:
        """Get character set by name and collation.

        Args:
            name: The charset name.
            collation: The collation name.

        Returns:
            Charset: The Charset dataclass instance.
        """
        try:
            return self._name_store[name][collation]
        except KeyError as err:
            raise ProgrammingError(
                f"Character set name '{name}' with collation '{collation}' not found"
            ) from err


MYSQL_8_CHARSETS = (
    (1, "big5", "big5_chinese_ci", True),
    (2, "latin2", "latin2_czech_cs", False),
    (3, "dec8", "dec8_swedish_ci", True),
    (4, "cp850", "cp850_general_ci", True),
    (5, "latin1", "latin1_german1_ci", False),
    (6, "hp8", "hp8_english_ci", True),
    (7, "koi8r", "koi8r_general_ci", True),
    (8, "latin1", "latin1_swedish_ci", True),
    (9, "latin2", "latin2_general_ci", True),
    (10, "swe7", "swe7_swedish_ci", True),
    (11, "ascii", "ascii_general_ci", True),
    (12, "ujis", "ujis_japanese_ci", True),
    (13, "sjis", "sjis_japanese_ci", True),
    (14, "cp1251", "cp1251_bulgarian_ci", False),
    (15, "latin1", "latin1_danish_ci", False),
    (16, "hebrew", "hebrew_general_ci", True),
    (18, "tis620", "tis620_thai_ci", True),
    (19, "euckr", "euckr_korean_ci", True),
    (20, "latin7", "latin7_estonian_cs", False),
    (21, "latin2", "latin2_hungarian_ci", False),
    (22, "koi8u", "koi8u_general_ci", True),
    (23, "cp1251", "cp1251_ukrainian_ci", False),
    (24, "gb2312", "gb2312_chinese_ci", True),
    (25, "greek", "greek_general_ci", True),
    (26, "cp1250", "cp1250_general_ci", True),
    (27, "latin2", "latin2_croatian_ci", False),
    (28, "gbk", "gbk_chinese_ci", True),
    (29, "cp1257", "cp1257_lithuanian_ci", False),
    (30, "latin5", "latin5_turkish_ci", True),
    (31, "latin1", "latin1_german2_ci", False),
    (32, "armscii8", "armscii8_general_ci", True),
    (33, "utf8mb3", "utf8mb3_general_ci", True),
    (34, "cp1250", "cp1250_czech_cs", False),
    (35, "ucs2", "ucs2_general_ci", True),
    (36, "cp866", "cp866_general_ci", True),
    (37, "keybcs2", "keybcs2_general_ci", True),
    (38, "macce", "macce_general_ci", True),
    (39, "macroman", "macroman_general_ci", True),
    (40, "cp852", "cp852_general_ci", True),
    (41, "latin7", "latin7_general_ci", True),
    (42, "latin7", "latin7_general_cs", False),
    (43, "macce", "macce_bin", False),
    (44, "cp1250", "cp1250_croatian_ci", False),
    (45, "utf8mb4", "utf8mb4_general_ci", False),
    (46, "utf8mb4", "utf8mb4_bin", False),
    (47, "latin1", "latin1_bin", False),
    (48, "latin1", "latin1_general_ci", False),
    (49, "latin1", "latin1_general_cs", False),
    (50, "cp1251", "cp1251_bin", False),
    (51, "cp1251", "cp1251_general_ci", True),
    (52, "cp1251", "cp1251_general_cs", False),
    (53, "macroman", "macroman_bin", False),
    (54, "utf16", "utf16_general_ci", True),
    (55, "utf16", "utf16_bin", False),
    (56, "utf16le", "utf16le_general_ci", True),
    (57, "cp1256", "cp1256_general_ci", True),
    (58, "cp1257", "cp1257_bin", False),
    (59, "cp1257", "cp1257_general_ci", True),
    (60, "utf32", "utf32_general_ci", True),
    (61, "utf32", "utf32_bin", False),
    (62, "utf16le", "utf16le_bin", False),
    (63, "binary", "binary", True),
    (64, "armscii8", "armscii8_bin", False),
    (65, "ascii", "ascii_bin", False),
    (66, "cp1250", "cp1250_bin", False),
    (67, "cp1256", "cp1256_bin", False),
    (68, "cp866", "cp866_bin", False),
    (69, "dec8", "dec8_bin", False),
    (70, "greek", "greek_bin", False),
    (71, "hebrew", "hebrew_bin", False),
    (72, "hp8", "hp8_bin", False),
    (73, "keybcs2", "keybcs2_bin", False),
    (74, "koi8r", "koi8r_bin", False),
    (75, "koi8u", "koi8u_bin", False),
    (76, "utf8mb3", "utf8mb3_tolower_ci", False),
    (77, "latin2", "latin2_bin", False),
    (78, "latin5", "latin5_bin", False),
    (79, "latin7", "latin7_bin", False),
    (80, "cp850", "cp850_bin", False),
    (81, "cp852", "cp852_bin", False),
    (82, "swe7", "swe7_bin", False),
    (83, "utf8mb3", "utf8mb3_bin", False),
    (84, "big5", "big5_bin", False),
    (85, "euckr", "euckr_bin", False),
    (86, "gb2312", "gb2312_bin", False),
    (87, "gbk", "gbk_bin", False),
    (88, "sjis", "sjis_bin", False),
    (89, "tis620", "tis620_bin", False),
    (90, "ucs2", "ucs2_bin", False),
    (91, "ujis", "ujis_bin", False),
    (92, "geostd8", "geostd8_general_ci", True),
    (93, "geostd8", "geostd8_bin", False),
    (94, "latin1", "latin1_spanish_ci", False),
    (95, "cp932", "cp932_japanese_ci", True),
    (96, "cp932", "cp932_bin", False),
    (97, "eucjpms", "eucjpms_japanese_ci", True),
    (98, "eucjpms", "eucjpms_bin", False),
    (99, "cp1250", "cp1250_polish_ci", False),
    (101, "utf16", "utf16_unicode_ci", False),
    (102, "utf16", "utf16_icelandic_ci", False),
    (103, "utf16", "utf16_latvian_ci", False),
    (104, "utf16", "utf16_romanian_ci", False),
    (105, "utf16", "utf16_slovenian_ci", False),
    (106, "utf16", "utf16_polish_ci", False),
    (107, "utf16", "utf16_estonian_ci", False),
    (108, "utf16", "utf16_spanish_ci", False),
    (109, "utf16", "utf16_swedish_ci", False),
    (110, "utf16", "utf16_turkish_ci", False),
    (111, "utf16", "utf16_czech_ci", False),
    (112, "utf16", "utf16_danish_ci", False),
    (113, "utf16", "utf16_lithuanian_ci", False),
    (114, "utf16", "utf16_slovak_ci", False),
    (115, "utf16", "utf16_spanish2_ci", False),
    (116, "utf16", "utf16_roman_ci", False),
    (117, "utf16", "utf16_persian_ci", False),
    (118, "utf16", "utf16_esperanto_ci", False),
    (119, "utf16", "utf16_hungarian_ci", False),
    (120, "utf16", "utf16_sinhala_ci", False),
    (121, "utf16", "utf16_german2_ci", False),
    (122, "utf16", "utf16_croatian_ci", False),
    (123, "utf16", "utf16_unicode_520_ci", False),
    (124, "utf16", "utf16_vietnamese_ci", False),
    (128, "ucs2", "ucs2_unicode_ci", False),
    (129, "ucs2", "ucs2_icelandic_ci", False),
    (130, "ucs2", "ucs2_latvian_ci", False),
    (131, "ucs2", "ucs2_romanian_ci", False),
    (132, "ucs2", "ucs2_slovenian_ci", False),
    (133, "ucs2", "ucs2_polish_ci", False),
    (134, "ucs2", "ucs2_estonian_ci", False),
    (135, "ucs2", "ucs2_spanish_ci", False),
    (136, "ucs2", "ucs2_swedish_ci", False),
    (137, "ucs2", "ucs2_turkish_ci", False),
    (138, "ucs2", "ucs2_czech_ci", False),
    (139, "ucs2", "ucs2_danish_ci", False),
    (140, "ucs2", "ucs2_lithuanian_ci", False),
    (141, "ucs2", "ucs2_slovak_ci", False),
    (142, "ucs2", "ucs2_spanish2_ci", False),
    (143, "ucs2", "ucs2_roman_ci", False),
    (144, "ucs2", "ucs2_persian_ci", False),
    (145, "ucs2", "ucs2_esperanto_ci", False),
    (146, "ucs2", "ucs2_hungarian_ci", False),
    (147, "ucs2", "ucs2_sinhala_ci", False),
    (148, "ucs2", "ucs2_german2_ci", False),
    (149, "ucs2", "ucs2_croatian_ci", False),
    (150, "ucs2", "ucs2_unicode_520_ci", False),
    (151, "ucs2", "ucs2_vietnamese_ci", False),
    (159, "ucs2", "ucs2_general_mysql500_ci", False),
    (160, "utf32", "utf32_unicode_ci", False),
    (161, "utf32", "utf32_icelandic_ci", False),
    (162, "utf32", "utf32_latvian_ci", False),
    (163, "utf32", "utf32_romanian_ci", False),
    (164, "utf32", "utf32_slovenian_ci", False),
    (165, "utf32", "utf32_polish_ci", False),
    (166, "utf32", "utf32_estonian_ci", False),
    (167, "utf32", "utf32_spanish_ci", False),
    (168, "utf32", "utf32_swedish_ci", False),
    (169, "utf32", "utf32_turkish_ci", False),
    (170, "utf32", "utf32_czech_ci", False),
    (171, "utf32", "utf32_danish_ci", False),
    (172, "utf32", "utf32_lithuanian_ci", False),
    (173, "utf32", "utf32_slovak_ci", False),
    (174, "utf32", "utf32_spanish2_ci", False),
    (175, "utf32", "utf32_roman_ci", False),
    (176, "utf32", "utf32_persian_ci", False),
    (177, "utf32", "utf32_esperanto_ci", False),
    (178, "utf32", "utf32_hungarian_ci", False),
    (179, "utf32", "utf32_sinhala_ci", False),
    (180, "utf32", "utf32_german2_ci", False),
    (181, "utf32", "utf32_croatian_ci", False),
    (182, "utf32", "utf32_unicode_520_ci", False),
    (183, "utf32", "utf32_vietnamese_ci", False),
    (192, "utf8mb3", "utf8mb3_unicode_ci", False),
    (193, "utf8mb3", "utf8mb3_icelandic_ci", False),
    (194, "utf8mb3", "utf8mb3_latvian_ci", False),
    (195, "utf8mb3", "utf8mb3_romanian_ci", False),
    (196, "utf8mb3", "utf8mb3_slovenian_ci", False),
    (197, "utf8mb3", "utf8mb3_polish_ci", False),
    (198, "utf8mb3", "utf8mb3_estonian_ci", False),
    (199, "utf8mb3", "utf8mb3_spanish_ci", False),
    (200, "utf8mb3", "utf8mb3_swedish_ci", False),
    (201, "utf8mb3", "utf8mb3_turkish_ci", False),
    (202, "utf8mb3", "utf8mb3_czech_ci", False),
    (203, "utf8mb3", "utf8mb3_danish_ci", False),
    (204, "utf8mb3", "utf8mb3_lithuanian_ci", False),
    (205, "utf8mb3", "utf8mb3_slovak_ci", False),
    (206, "utf8mb3", "utf8mb3_spanish2_ci", False),
    (207, "utf8mb3", "utf8mb3_roman_ci", False),
    (208, "utf8mb3", "utf8mb3_persian_ci", False),
    (209, "utf8mb3", "utf8mb3_esperanto_ci", False),
    (210, "utf8mb3", "utf8mb3_hungarian_ci", False),
    (211, "utf8mb3", "utf8mb3_sinhala_ci", False),
    (212, "utf8mb3", "utf8mb3_german2_ci", False),
    (213, "utf8mb3", "utf8mb3_croatian_ci", False),
    (214, "utf8mb3", "utf8mb3_unicode_520_ci", False),
    (215, "utf8mb3", "utf8mb3_vietnamese_ci", False),
    (223, "utf8mb3", "utf8mb3_general_mysql500_ci", False),
    (224, "utf8mb4", "utf8mb4_unicode_ci", False),
    (225, "utf8mb4", "utf8mb4_icelandic_ci", False),
    (226, "utf8mb4", "utf8mb4_latvian_ci", False),
    (227, "utf8mb4", "utf8mb4_romanian_ci", False),
    (228, "utf8mb4", "utf8mb4_slovenian_ci", False),
    (229, "utf8mb4", "utf8mb4_polish_ci", False),
    (230, "utf8mb4", "utf8mb4_estonian_ci", False),
    (231, "utf8mb4", "utf8mb4_spanish_ci", False),
    (232, "utf8mb4", "utf8mb4_swedish_ci", False),
    (233, "utf8mb4", "utf8mb4_turkish_ci", False),
    (234, "utf8mb4", "utf8mb4_czech_ci", False),
    (235, "utf8mb4", "utf8mb4_danish_ci", False),
    (236, "utf8mb4", "utf8mb4_lithuanian_ci", False),
    (237, "utf8mb4", "utf8mb4_slovak_ci", False),
    (238, "utf8mb4", "utf8mb4_spanish2_ci", False),
    (239, "utf8mb4", "utf8mb4_roman_ci", False),
    (240, "utf8mb4", "utf8mb4_persian_ci", False),
    (241, "utf8mb4", "utf8mb4_esperanto_ci", False),
    (242, "utf8mb4", "utf8mb4_hungarian_ci", False),
    (243, "utf8mb4", "utf8mb4_sinhala_ci", False),
    (244, "utf8mb4", "utf8mb4_german2_ci", False),
    (245, "utf8mb4", "utf8mb4_croatian_ci", False),
    (246, "utf8mb4", "utf8mb4_unicode_520_ci", False),
    (247, "utf8mb4", "utf8mb4_vietnamese_ci", False),
    (248, "gb18030", "gb18030_chinese_ci", True),
    (249, "gb18030", "gb18030_bin", False),
    (250, "gb18030", "gb18030_unicode_520_ci", False),
    (255, "utf8mb4", "utf8mb4_0900_ai_ci", True),
    (256, "utf8mb4", "utf8mb4_de_pb_0900_ai_ci", False),
    (257, "utf8mb4", "utf8mb4_is_0900_ai_ci", False),
    (258, "utf8mb4", "utf8mb4_lv_0900_ai_ci", False),
    (259, "utf8mb4", "utf8mb4_ro_0900_ai_ci", False),
    (260, "utf8mb4", "utf8mb4_sl_0900_ai_ci", False),
    (261, "utf8mb4", "utf8mb4_pl_0900_ai_ci", False),
    (262, "utf8mb4", "utf8mb4_et_0900_ai_ci", False),
    (263, "utf8mb4", "utf8mb4_es_0900_ai_ci", False),
    (264, "utf8mb4", "utf8mb4_sv_0900_ai_ci", False),
    (265, "utf8mb4", "utf8mb4_tr_0900_ai_ci", False),
    (266, "utf8mb4", "utf8mb4_cs_0900_ai_ci", False),
    (267, "utf8mb4", "utf8mb4_da_0900_ai_ci", False),
    (268, "utf8mb4", "utf8mb4_lt_0900_ai_ci", False),
    (269, "utf8mb4", "utf8mb4_sk_0900_ai_ci", False),
    (270, "utf8mb4", "utf8mb4_es_trad_0900_ai_ci", False),
    (271, "utf8mb4", "utf8mb4_la_0900_ai_ci", False),
    (273, "utf8mb4", "utf8mb4_eo_0900_ai_ci", False),
    (274, "utf8mb4", "utf8mb4_hu_0900_ai_ci", False),
    (275, "utf8mb4", "utf8mb4_hr_0900_ai_ci", False),
    (277, "utf8mb4", "utf8mb4_vi_0900_ai_ci", False),
    (278, "utf8mb4", "utf8mb4_0900_as_cs", False),
    (279, "utf8mb4", "utf8mb4_de_pb_0900_as_cs", False),
    (280, "utf8mb4", "utf8mb4_is_0900_as_cs", False),
    (281, "utf8mb4", "utf8mb4_lv_0900_as_cs", False),
    (282, "utf8mb4", "utf8mb4_ro_0900_as_cs", False),
    (283, "utf8mb4", "utf8mb4_sl_0900_as_cs", False),
    (284, "utf8mb4", "utf8mb4_pl_0900_as_cs", False),
    (285, "utf8mb4", "utf8mb4_et_0900_as_cs", False),
    (286, "utf8mb4", "utf8mb4_es_0900_as_cs", False),
    (287, "utf8mb4", "utf8mb4_sv_0900_as_cs", False),
    (288, "utf8mb4", "utf8mb4_tr_0900_as_cs", False),
    (289, "utf8mb4", "utf8mb4_cs_0900_as_cs", False),
    (290, "utf8mb4", "utf8mb4_da_0900_as_cs", False),
    (291, "utf8mb4", "utf8mb4_lt_0900_as_cs", False),
    (292, "utf8mb4", "utf8mb4_sk_0900_as_cs", False),
    (293, "utf8mb4", "utf8mb4_es_trad_0900_as_cs", False),
    (294, "utf8mb4", "utf8mb4_la_0900_as_cs", False),
    (296, "utf8mb4", "utf8mb4_eo_0900_as_cs", False),
    (297, "utf8mb4", "utf8mb4_hu_0900_as_cs", False),
    (298, "utf8mb4", "utf8mb4_hr_0900_as_cs", False),
    (300, "utf8mb4", "utf8mb4_vi_0900_as_cs", False),
    (303, "utf8mb4", "utf8mb4_ja_0900_as_cs", False),
    (304, "utf8mb4", "utf8mb4_ja_0900_as_cs_ks", False),
    (305, "utf8mb4", "utf8mb4_0900_as_ci", False),
    (306, "utf8mb4", "utf8mb4_ru_0900_ai_ci", False),
    (307, "utf8mb4", "utf8mb4_ru_0900_as_cs", False),
    (308, "utf8mb4", "utf8mb4_zh_0900_as_cs", False),
    (309, "utf8mb4", "utf8mb4_0900_bin", False),
    (310, "utf8mb4", "utf8mb4_nb_0900_ai_ci", False),
    (311, "utf8mb4", "utf8mb4_nb_0900_as_cs", False),
    (312, "utf8mb4", "utf8mb4_nn_0900_ai_ci", False),
    (313, "utf8mb4", "utf8mb4_nn_0900_as_cs", False),
    (314, "utf8mb4", "utf8mb4_sr_latn_0900_ai_ci", False),
    (315, "utf8mb4", "utf8mb4_sr_latn_0900_as_cs", False),
    (316, "utf8mb4", "utf8mb4_bs_0900_ai_ci", False),
    (317, "utf8mb4", "utf8mb4_bs_0900_as_cs", False),
    (318, "utf8mb4", "utf8mb4_bg_0900_ai_ci", False),
    (319, "utf8mb4", "utf8mb4_bg_0900_as_cs", False),
    (320, "utf8mb4", "utf8mb4_gl_0900_ai_ci", False),
    (321, "utf8mb4", "utf8mb4_gl_0900_as_cs", False),
    (322, "utf8mb4", "utf8mb4_mn_cyrl_0900_ai_ci", False),
    (323, "utf8mb4", "utf8mb4_mn_cyrl_0900_as_cs", False),
)

MYSQL_5_CHARSETS = (
    (1, "big5", "big5_chinese_ci", True),
    (2, "latin2", "latin2_czech_cs", False),
    (3, "dec8", "dec8_swedish_ci", True),
    (4, "cp850", "cp850_general_ci", True),
    (5, "latin1", "latin1_german1_ci", False),
    (6, "hp8", "hp8_english_ci", True),
    (7, "koi8r", "koi8r_general_ci", True),
    (8, "latin1", "latin1_swedish_ci", True),
    (9, "latin2", "latin2_general_ci", True),
    (10, "swe7", "swe7_swedish_ci", True),
    (11, "ascii", "ascii_general_ci", True),
    (12, "ujis", "ujis_japanese_ci", True),
    (13, "sjis", "sjis_japanese_ci", True),
    (14, "cp1251", "cp1251_bulgarian_ci", False),
    (15, "latin1", "latin1_danish_ci", False),
    (16, "hebrew", "hebrew_general_ci", True),
    (18, "tis620", "tis620_thai_ci", True),
    (19, "euckr", "euckr_korean_ci", True),
    (20, "latin7", "latin7_estonian_cs", False),
    (21, "latin2", "latin2_hungarian_ci", False),
    (22, "koi8u", "koi8u_general_ci", True),
    (23, "cp1251", "cp1251_ukrainian_ci", False),
    (24, "gb2312", "gb2312_chinese_ci", True),
    (25, "greek", "greek_general_ci", True),
    (26, "cp1250", "cp1250_general_ci", True),
    (27, "latin2", "latin2_croatian_ci", False),
    (28, "gbk", "gbk_chinese_ci", True),
    (29, "cp1257", "cp1257_lithuanian_ci", False),
    (30, "latin5", "latin5_turkish_ci", True),
    (31, "latin1", "latin1_german2_ci", False),
    (32, "armscii8", "armscii8_general_ci", True),
    (33, "utf8", "utf8_general_ci", True),
    (34, "cp1250", "cp1250_czech_cs", False),
    (35, "ucs2", "ucs2_general_ci", True),
    (36, "cp866", "cp866_general_ci", True),
    (37, "keybcs2", "keybcs2_general_ci", True),
    (38, "macce", "macce_general_ci", True),
    (39, "macroman", "macroman_general_ci", True),
    (40, "cp852", "cp852_general_ci", True),
    (41, "latin7", "latin7_general_ci", True),
    (42, "latin7", "latin7_general_cs", False),
    (43, "macce", "macce_bin", False),
    (44, "cp1250", "cp1250_croatian_ci", False),
    (45, "utf8mb4", "utf8mb4_general_ci", True),
    (46, "utf8mb4", "utf8mb4_bin", False),
    (47, "latin1", "latin1_bin", False),
    (48, "latin1", "latin1_general_ci", False),
    (49, "latin1", "latin1_general_cs", False),
    (50, "cp1251", "cp1251_bin", False),
    (51, "cp1251", "cp1251_general_ci", True),
    (52, "cp1251", "cp1251_general_cs", False),
    (53, "macroman", "macroman_bin", False),
    (54, "utf16", "utf16_general_ci", True),
    (55, "utf16", "utf16_bin", False),
    (56, "utf16le", "utf16le_general_ci", True),
    (57, "cp1256", "cp1256_general_ci", True),
    (58, "cp1257", "cp1257_bin", False),
    (59, "cp1257", "cp1257_general_ci", True),
    (60, "utf32", "utf32_general_ci", True),
    (61, "utf32", "utf32_bin", False),
    (62, "utf16le", "utf16le_bin", False),
    (63, "binary", "binary", True),
    (64, "armscii8", "armscii8_bin", False),
    (65, "ascii", "ascii_bin", False),
    (66, "cp1250", "cp1250_bin", False),
    (67, "cp1256", "cp1256_bin", False),
    (68, "cp866", "cp866_bin", False),
    (69, "dec8", "dec8_bin", False),
    (70, "greek", "greek_bin", False),
    (71, "hebrew", "hebrew_bin", False),
    (72, "hp8", "hp8_bin", False),
    (73, "keybcs2", "keybcs2_bin", False),
    (74, "koi8r", "koi8r_bin", False),
    (75, "koi8u", "koi8u_bin", False),
    (77, "latin2", "latin2_bin", False),
    (78, "latin5", "latin5_bin", False),
    (79, "latin7", "latin7_bin", False),
    (80, "cp850", "cp850_bin", False),
    (81, "cp852", "cp852_bin", False),
    (82, "swe7", "swe7_bin", False),
    (83, "utf8", "utf8_bin", False),
    (84, "big5", "big5_bin", False),
    (85, "euckr", "euckr_bin", False),
    (86, "gb2312", "gb2312_bin", False),
    (87, "gbk", "gbk_bin", False),
    (88, "sjis", "sjis_bin", False),
    (89, "tis620", "tis620_bin", False),
    (90, "ucs2", "ucs2_bin", False),
    (91, "ujis", "ujis_bin", False),
    (92, "geostd8", "geostd8_general_ci", True),
    (93, "geostd8", "geostd8_bin", False),
    (94, "latin1", "latin1_spanish_ci", False),
    (95, "cp932", "cp932_japanese_ci", True),
    (96, "cp932", "cp932_bin", False),
    (97, "eucjpms", "eucjpms_japanese_ci", True),
    (98, "eucjpms", "eucjpms_bin", False),
    (99, "cp1250", "cp1250_polish_ci", False),
    (101, "utf16", "utf16_unicode_ci", False),
    (102, "utf16", "utf16_icelandic_ci", False),
    (103, "utf16", "utf16_latvian_ci", False),
    (104, "utf16", "utf16_romanian_ci", False),
    (105, "utf16", "utf16_slovenian_ci", False),
    (106, "utf16", "utf16_polish_ci", False),
    (107, "utf16", "utf16_estonian_ci", False),
    (108, "utf16", "utf16_spanish_ci", False),
    (109, "utf16", "utf16_swedish_ci", False),
    (110, "utf16", "utf16_turkish_ci", False),
    (111, "utf16", "utf16_czech_ci", False),
    (112, "utf16", "utf16_danish_ci", False),
    (113, "utf16", "utf16_lithuanian_ci", False),
    (114, "utf16", "utf16_slovak_ci", False),
    (115, "utf16", "utf16_spanish2_ci", False),
    (116, "utf16", "utf16_roman_ci", False),
    (117, "utf16", "utf16_persian_ci", False),
    (118, "utf16", "utf16_esperanto_ci", False),
    (119, "utf16", "utf16_hungarian_ci", False),
    (120, "utf16", "utf16_sinhala_ci", False),
    (121, "utf16", "utf16_german2_ci", False),
    (122, "utf16", "utf16_croatian_ci", False),
    (123, "utf16", "utf16_unicode_520_ci", False),
    (124, "utf16", "utf16_vietnamese_ci", False),
    (128, "ucs2", "ucs2_unicode_ci", False),
    (129, "ucs2", "ucs2_icelandic_ci", False),
    (130, "ucs2", "ucs2_latvian_ci", False),
    (131, "ucs2", "ucs2_romanian_ci", False),
    (132, "ucs2", "ucs2_slovenian_ci", False),
    (133, "ucs2", "ucs2_polish_ci", False),
    (134, "ucs2", "ucs2_estonian_ci", False),
    (135, "ucs2", "ucs2_spanish_ci", False),
    (136, "ucs2", "ucs2_swedish_ci", False),
    (137, "ucs2", "ucs2_turkish_ci", False),
    (138, "ucs2", "ucs2_czech_ci", False),
    (139, "ucs2", "ucs2_danish_ci", False),
    (140, "ucs2", "ucs2_lithuanian_ci", False),
    (141, "ucs2", "ucs2_slovak_ci", False),
    (142, "ucs2", "ucs2_spanish2_ci", False),
    (143, "ucs2", "ucs2_roman_ci", False),
    (144, "ucs2", "ucs2_persian_ci", False),
    (145, "ucs2", "ucs2_esperanto_ci", False),
    (146, "ucs2", "ucs2_hungarian_ci", False),
    (147, "ucs2", "ucs2_sinhala_ci", False),
    (148, "ucs2", "ucs2_german2_ci", False),
    (149, "ucs2", "ucs2_croatian_ci", False),
    (150, "ucs2", "ucs2_unicode_520_ci", False),
    (151, "ucs2", "ucs2_vietnamese_ci", False),
    (159, "ucs2", "ucs2_general_mysql500_ci", False),
    (160, "utf32", "utf32_unicode_ci", False),
    (161, "utf32", "utf32_icelandic_ci", False),
    (162, "utf32", "utf32_latvian_ci", False),
    (163, "utf32", "utf32_romanian_ci", False),
    (164, "utf32", "utf32_slovenian_ci", False),
    (165, "utf32", "utf32_polish_ci", False),
    (166, "utf32", "utf32_estonian_ci", False),
    (167, "utf32", "utf32_spanish_ci", False),
    (168, "utf32", "utf32_swedish_ci", False),
    (169, "utf32", "utf32_turkish_ci", False),
    (170, "utf32", "utf32_czech_ci", False),
    (171, "utf32", "utf32_danish_ci", False),
    (172, "utf32", "utf32_lithuanian_ci", False),
    (173, "utf32", "utf32_slovak_ci", False),
    (174, "utf32", "utf32_spanish2_ci", False),
    (175, "utf32", "utf32_roman_ci", False),
    (176, "utf32", "utf32_persian_ci", False),
    (177, "utf32", "utf32_esperanto_ci", False),
    (178, "utf32", "utf32_hungarian_ci", False),
    (179, "utf32", "utf32_sinhala_ci", False),
    (180, "utf32", "utf32_german2_ci", False),
    (181, "utf32", "utf32_croatian_ci", False),
    (182, "utf32", "utf32_unicode_520_ci", False),
    (183, "utf32", "utf32_vietnamese_ci", False),
    (192, "utf8", "utf8_unicode_ci", False),
    (193, "utf8", "utf8_icelandic_ci", False),
    (194, "utf8", "utf8_latvian_ci", False),
    (195, "utf8", "utf8_romanian_ci", False),
    (196, "utf8", "utf8_slovenian_ci", False),
    (197, "utf8", "utf8_polish_ci", False),
    (198, "utf8", "utf8_estonian_ci", False),
    (199, "utf8", "utf8_spanish_ci", False),
    (200, "utf8", "utf8_swedish_ci", False),
    (201, "utf8", "utf8_turkish_ci", False),
    (202, "utf8", "utf8_czech_ci", False),
    (203, "utf8", "utf8_danish_ci", False),
    (204, "utf8", "utf8_lithuanian_ci", False),
    (205, "utf8", "utf8_slovak_ci", False),
    (206, "utf8", "utf8_spanish2_ci", False),
    (207, "utf8", "utf8_roman_ci", False),
    (208, "utf8", "utf8_persian_ci", False),
    (209, "utf8", "utf8_esperanto_ci", False),
    (210, "utf8", "utf8_hungarian_ci", False),
    (211, "utf8", "utf8_sinhala_ci", False),
    (212, "utf8", "utf8_german2_ci", False),
    (213, "utf8", "utf8_croatian_ci", False),
    (214, "utf8", "utf8_unicode_520_ci", False),
    (215, "utf8", "utf8_vietnamese_ci", False),
    (223, "utf8", "utf8_general_mysql500_ci", False),
    (224, "utf8mb4", "utf8mb4_unicode_ci", False),
    (225, "utf8mb4", "utf8mb4_icelandic_ci", False),
    (226, "utf8mb4", "utf8mb4_latvian_ci", False),
    (227, "utf8mb4", "utf8mb4_romanian_ci", False),
    (228, "utf8mb4", "utf8mb4_slovenian_ci", False),
    (229, "utf8mb4", "utf8mb4_polish_ci", False),
    (230, "utf8mb4", "utf8mb4_estonian_ci", False),
    (231, "utf8mb4", "utf8mb4_spanish_ci", False),
    (232, "utf8mb4", "utf8mb4_swedish_ci", False),
    (233, "utf8mb4", "utf8mb4_turkish_ci", False),
    (234, "utf8mb4", "utf8mb4_czech_ci", False),
    (235, "utf8mb4", "utf8mb4_danish_ci", False),
    (236, "utf8mb4", "utf8mb4_lithuanian_ci", False),
    (237, "utf8mb4", "utf8mb4_slovak_ci", False),
    (238, "utf8mb4", "utf8mb4_spanish2_ci", False),
    (239, "utf8mb4", "utf8mb4_roman_ci", False),
    (240, "utf8mb4", "utf8mb4_persian_ci", False),
    (241, "utf8mb4", "utf8mb4_esperanto_ci", False),
    (242, "utf8mb4", "utf8mb4_hungarian_ci", False),
    (243, "utf8mb4", "utf8mb4_sinhala_ci", False),
    (244, "utf8mb4", "utf8mb4_german2_ci", False),
    (245, "utf8mb4", "utf8mb4_croatian_ci", False),
    (246, "utf8mb4", "utf8mb4_unicode_520_ci", False),
    (247, "utf8mb4", "utf8mb4_vietnamese_ci", False),
    (248, "gb18030", "gb18030_chinese_ci", True),
    (249, "gb18030", "gb18030_bin", False),
    (250, "gb18030", "gb18030_unicode_520_ci", False),
)

charsets = Charsets()
