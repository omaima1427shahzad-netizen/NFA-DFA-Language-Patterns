"""
Unit tests for NFA to DFA converter
"""

import pytest
import sys
sys.path.insert(0, '..')

from src.nfa import NFA
from src.converter import NFAToDFAConverter


class TestConverterBasic:
    """Test basic NFA to DFA conversion"""
    
    @pytest.fixture
    def simple_nfa(self):
        """Create a simple NFA"""
        return NFA(
            states={'q0', 'q1', 'q2'},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'a'): {'q0', 'q1'},
                ('q0', 'b'): {'q0'},
                ('q1', 'b'): {'q2'},
            },
            start_state='q0',
            accept_states={'q2'}
        )
    
    def test_converter_creates_dfa(self, simple_nfa):
        """Test that converter creates a valid DFA"""
        converter = NFAToDFAConverter(simple_nfa)
        dfa = converter.convert()
        assert dfa is not None
        assert len(dfa.states) > 0
        assert dfa.start_state is not None
    
    def test_dfa_accepts_same_strings(self, simple_nfa):
        """Test that converted DFA accepts same strings as NFA"""
        converter = NFAToDFAConverter(simple_nfa)
        dfa = converter.convert()
        
        test_strings = ["ab", "aab", "aaab", "a", "b", "ba"]
        
        for test_str in test_strings:
            nfa_result = simple_nfa.accepts(test_str)
            dfa_result = dfa.accepts(test_str)
            assert nfa_result == dfa_result, f"Mismatch for '{test_str}'"


class TestConverterWithEpsilon:
    """Test conversion of NFA with epsilon transitions"""
    
    @pytest.fixture
    def epsilon_nfa(self):
        """NFA with epsilon transitions"""
        return NFA(
            states={'q0', 'q1', 'q2', 'q3'},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'ε'): {'q1', 'q2'},
                ('q1', 'a'): {'q3'},
                ('q2', 'b'): {'q3'},
            },
            start_state='q0',
            accept_states={'q3'}
        )
    
    def test_epsilon_nfa_conversion(self, epsilon_nfa):
        """Test conversion of NFA with epsilon transitions"""
        converter = NFAToDFAConverter(epsilon_nfa)
        dfa = converter.convert()
        
        # Test acceptance equivalence
        test_strings = ["a", "b", "ab", "ba", "", "aa"]
        
        for test_str in test_strings:
            nfa_result = epsilon_nfa.accepts(test_str)
            dfa_result = dfa.accepts(test_str)
            assert nfa_result == dfa_result


class TestConverterMultiplePaths:
    """Test conversion of NFA with multiple paths"""
    
    @pytest.fixture
    def multi_path_nfa(self):
        """NFA with multiple possible paths"""
        return NFA(
            states={'q0', 'q1', 'q2', 'q3'},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'a'): {'q1', 'q2'},
                ('q1', 'a'): {'q1'},
                ('q1', 'b'): {'q3'},
                ('q2', 'a'): {'q2'},
                ('q2', 'b'): {'q3'},
            },
            start_state='q0',
            accept_states={'q3'}
        )
    
    def test_multi_path_conversion(self, multi_path_nfa):
        """Test conversion of multi-path NFA"""
        converter = NFAToDFAConverter(multi_path_nfa)
        dfa = converter.convert()
        
        test_strings = ["ab", "aab", "aaab", "aabb", "aa", "b", ""]
        
        for test_str in test_strings:
            nfa_result = multi_path_nfa.accepts(test_str)
            dfa_result = dfa.accepts(test_str)
            assert nfa_result == dfa_result


class TestConverterProperties:
    """Test converter properties and structure"""
    
    @pytest.fixture
    def simple_nfa(self):
        return NFA(
            states={'q0', 'q1', 'q2'},
            alphabet={'0', '1'},
            transitions={
                ('q0', '0'): {'q0', 'q1'},
                ('q0', '1'): {'q0'},
                ('q1', '1'): {'q2'},
            },
            start_state='q0',
            accept_states={'q2'}
        )
    
    def test_dfa_completeness(self, simple_nfa):
        """Test that converted DFA is complete"""
        converter = NFAToDFAConverter(simple_nfa)
        dfa = converter.convert()
        
        # Check that all states have transitions for all symbols
        for state in dfa.states:
            for symbol in dfa.alphabet:
                assert (state, symbol) in dfa.transitions, \
                    f"Missing transition from {state} on {symbol}"
    
    def test_dfa_determinism(self, simple_nfa):
        """Test that converted DFA is deterministic"""
        converter = NFAToDFAConverter(simple_nfa)
        dfa = converter.convert()
        
        # Check that each transition leads to exactly one state
        for (state, symbol), next_state in dfa.transitions.items():
            assert isinstance(next_state, str), \
                f"Transition from {state} on {symbol} should lead to one state"


class TestConverterStateMapping:
    """Test state mapping in converter"""
    
    @pytest.fixture
    def simple_nfa(self):
        return NFA(
            states={'q0', 'q1'},
            alphabet={'a'},
            transitions={
                ('q0', 'a'): {'q0', 'q1'},
            },
            start_state='q0',
            accept_states={'q1'}
        )
    
    def test_state_mapping_exists(self, simple_nfa):
        """Test that state mapping is available"""
        converter = NFAToDFAConverter(simple_nfa)
        dfa = converter.convert()
        mapping = converter.get_state_mapping()
        assert len(mapping) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
