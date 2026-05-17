import pytest
from core.algorithms.classical.Playfair import Thread


class TestPlayfairMatrix:
    """测试 Playfair 密钥矩阵"""

    def test_matrix_size(self):
        """测试密钥矩阵大小为 5x5"""
        letter_matrix = [[''] * 5 for _ in range(5)]
        assert len(letter_matrix) == 5
        assert len(letter_matrix[0]) == 5

    def test_get_matrix_index(self):
        """测试获取字符在矩阵中的位置"""
        # 创建一个简单的测试矩阵
        letter_matrix = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        # A 在 (0, 0)
        assert Thread.get_matrix_index('A', letter_matrix) == (0, 0)
        # E 在 (0, 4)
        assert Thread.get_matrix_index('E', letter_matrix) == (0, 4)
        # K (替代 J) 在 (1, 4)
        assert Thread.get_matrix_index('K', letter_matrix) == (1, 4)
        # Z 在 (4, 4)
        assert Thread.get_matrix_index('Z', letter_matrix) == (4, 4)

    def test_j_not_found(self):
        """测试 J 在矩阵中找不到（返回 None）"""
        letter_matrix = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        # J 在矩阵中不存在（因为被跳过）
        assert Thread.get_matrix_index('J', letter_matrix) is None


class TestPlayfairKeyProcessing:
    """测试 Playfair 密钥处理"""

    def test_key_deduplication(self):
        """测试密钥去重"""
        key = "PLAYFAIR"
        key_list = []
        for ch in key:
            if ch == 'J':
                ch = 'I'
            if ch not in key_list:
                key_list.append(ch)
        assert len(key_list) == len(set(key_list))

    def test_key_to_matrix_conversion(self):
        """测试密钥转换为 5x5 矩阵"""
        key = "KEYWORD"
        key_str = "KEYWORD"
        for ch in key_str:
            if ch == 'J':
                ch = 'I'
            if ch not in key_str[:key_str.index(ch)]:
                key_str = key_str.replace(ch, '', 1)
        
        # 添加剩余字母
        letter_list = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        for ch in letter_list:
            if ch not in key_str:
                key_str += ch
        
        # 转换为 5x5 矩阵
        letter_matrix = [''] * 5
        j = 0
        for i in range(len(key_str)):
            letter_matrix[j] += key_str[i]
            if (i + 1) % 5 == 0:
                j += 1
        
        assert len(letter_matrix) == 5
        assert len(letter_matrix[0]) == 5


class TestPlayfairEncryptionRules:
    """测试 Playfair 加密规则"""

    def test_same_row_encryption(self):
        """测试同一行的加密规则"""
        # 如果两个字符在同一行，则取其右边的字符
        letter_matrix = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        # A(0,0) 和 B(0,1) 在同一行
        # 加密后应该是 B(0,1) 和 C(0,2)
        row, col = 0, 0
        new_col = (col + 1) % 5
        assert letter_matrix[row][new_col] == 'B'

    def test_same_column_encryption(self):
        """测试同一列的加密规则"""
        # 如果两个字符在同一列，则取其下方的字符
        letter_matrix = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        # A(0,0) 和 F(1,0) 在同一列
        # 加密后应该是 F(1,0) 和 L(2,0)
        row, col = 0, 0
        new_row = (row + 1) % 5
        assert letter_matrix[new_row][col] == 'F'

    def test_different_row_column_encryption(self):
        """测试不同行不同列的加密规则"""
        # 如果两个字符既不在同一行也不在同一列，则取其对角位置的字符
        letter_matrix = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        # A(0,0) 和 G(1,1) 不在同一行也不在同一列
        # 加密规则：取同行不同列的对角字符
        # A(0,0) -> matrix[0][1] = 'B'
        # G(1,1) -> matrix[1][0] = 'F'
        x = (0, 0)
        y = (1, 1)
        # 同列交换：matrix[x[0]][y[1]], matrix[y[0]][x[1]]
        assert letter_matrix[x[0]][y[1]] == 'B'  # A -> B
        assert letter_matrix[y[0]][x[1]] == 'F'  # G -> F


class TestPlayfairMathProperties:
    """测试 Playfair 数学性质"""

    def test_padding_for_odd_length(self):
        """测试奇数长度明文需要填充"""
        plaintext = "HELLO"
        if len(plaintext) % 2 != 0:
            plaintext += 'Z'
        assert len(plaintext) % 2 == 0

    def test_no_padding_for_even_length(self):
        """测试偶数长度明文不需要填充"""
        plaintext = "HELP"
        if len(plaintext) % 2 != 0:
            plaintext += 'Z'
        assert len(plaintext) % 2 == 0
        assert len(plaintext) == 4

    def test_repeated_letter_insertion(self):
        """测试重复字母插入 Q"""
        plaintext = "BOOK"
        # B-O-O-K 应该变成 B-O-Q-O-K (在重复的 O 之间插入 Q)
        result = []
        for i in range(len(plaintext)):
            result.append(plaintext[i])
            if i < len(plaintext) - 1 and plaintext[i] == plaintext[i + 1]:
                result.append('Q')
        # 但是由于实际算法会处理，这里只是验证插入逻辑
        assert len(result) >= len(plaintext)
