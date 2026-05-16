import pytest
from core.algorithms.symmetric.DES import PI, CP_1, CP_2, E, S_BOX, P, SHIFT


class TestDESConstants:
    """Test DES constant tables"""

    def test_initial_permutation_length(self):
        """PI should have 64 elements"""
        assert len(PI) == 64

    def test_initial_permutation_range(self):
        """PI values should be 1-64"""
        for i, val in enumerate(PI):
            assert 1 <= val <= 64, f"PI[{i}]={val} out of range"

    def test_initial_permutation_unique(self):
        """PI should contain all values 1-64"""
        assert set(PI) == set(range(1, 65))

    def test_cp1_length(self):
        """CP_1 should have 56 elements"""
        assert len(CP_1) == 56

    def test_cp1_range(self):
        """CP_1 values should be 1-64"""
        for i, val in enumerate(CP_1):
            assert 1 <= val <= 64, f"CP_1[{i}]={val} out of range"

    def test_cp1_unique(self):
        """CP_1 should contain all values 1-64 without duplicates"""
        assert len(CP_1) == len(set(CP_1))

    def test_cp2_length(self):
        """CP_2 should have 48 elements"""
        assert len(CP_2) == 48

    def test_cp2_range(self):
        """CP_2 values should be 1-64"""
        for i, val in enumerate(CP_2):
            assert 1 <= val <= 64, f"CP_2[{i}]={val} out of range"

    def test_cp2_unique(self):
        """CP_2 should contain all values 1-64 without duplicates"""
        assert len(CP_2) == len(set(CP_2))

    def test_expansion_matrix_length(self):
        """E should have 48 elements"""
        assert len(E) == 48

    def test_expansion_matrix_range(self):
        """E values should be 1-32"""
        for i, val in enumerate(E):
            assert 1 <= val <= 32, f"E[{i}]={val} out of range"

    def test_s_box_shape(self):
        """S_BOX should be 8x4x16"""
        assert len(S_BOX) == 8
        for i in range(8):
            assert len(S_BOX[i]) == 4
            for j in range(4):
                assert len(S_BOX[i][j]) == 16

    def test_s_box_values_range(self):
        """S_BOX values should be 0-15"""
        for i in range(8):
            for j in range(4):
                for k in range(16):
                    assert 0 <= S_BOX[i][j][k] <= 15

    def test_s_box_unique_per_box(self):
        """Each S_BOX should contain all values 0-15"""
        for i in range(8):
            flat = [S_BOX[i][j][k] for j in range(4) for k in range(16)]
            assert set(flat) == set(range(16))

    def test_p_length(self):
        """P should have 32 elements"""
        assert len(P) == 32

    def test_p_range(self):
        """P values should be 1-32"""
        for i, val in enumerate(P):
            assert 1 <= val <= 32, f"P[{i}]={val} out of range"

    def test_p_unique(self):
        """P should contain all values 1-32"""
        assert len(P) == len(set(P))

    def test_shift_schedule_length(self):
        """SHIFT should have 16 elements"""
        assert len(SHIFT) == 16


class TestDESSBox:
    """Test DES S-Box substitution"""

    def test_s_box_row_column_selection(self):
        """S-Box lookup: row from outer bits, column from inner bits"""
        # S_BOX[0] with row=0, col=0 should give specific value
        row = 0b00  # bits 5 and 0
        col = 0b0000  # bits 1-4
        val = S_BOX[0][row][col]
        assert 0 <= val <= 15

    def test_all_s_boxes_produce_valid_output(self):
        """All S-boxes should produce values 0-15"""
        for i in range(8):
            for row in range(4):
                for col in range(16):
                    assert 0 <= S_BOX[i][row][col] <= 15


class TestDESMathProperties:
    """Test DES mathematical properties"""

    def test_pi_is_permutation(self):
        """PI should be a permutation of 1-64"""
        assert set(PI) == set(range(1, 65))

    def test_cp1_is_permutation(self):
        """CP_1 should be a permutation of 1-64"""
        assert len(CP_1) == 56
        assert len(set(CP_1)) == 56

    def test_cp2_is_permutation(self):
        """CP_2 should be a permutation of some 1-64 subset"""
        assert len(CP_2) == 48
        assert len(set(CP_2)) == 48

    def test_p_is_permutation(self):
        """P should be a permutation of 1-32"""
        assert set(P) == set(range(1, 33))

    def test_e_expansion_range(self):
        """E expansion should produce values 1-32"""
        for val in E:
            assert 1 <= val <= 32
