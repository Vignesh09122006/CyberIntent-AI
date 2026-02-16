"""Tests for data generators."""

import pytest
import pandas as pd
from data.generators.normal_user import NormalUserBehaviorGenerator
from data.generators.attacker import AttackerBehaviorGenerator
from data.generators.network_simulator import NetworkSimulator


def test_normal_user_generator():
    """Test normal user behavior generator."""
    gen = NormalUserBehaviorGenerator()
    session = gen.generate_session('test_user')
    
    assert isinstance(session, pd.DataFrame)
    assert len(session) > 0
    assert 'timestamp' in session.columns


def test_normal_user_batch():
    """Test batch generation."""
    gen = NormalUserBehaviorGenerator()
    batch = gen.generate_batch(num_users=5, sessions_per_user=2)
    
    assert isinstance(batch, pd.DataFrame)
    assert len(batch) > 0


def test_attacker_port_scan():
    """Test port scan generation."""
    gen = AttackerBehaviorGenerator()
    scan = gen.generate_port_scan('203.0.113.1')
    
    assert isinstance(scan, pd.DataFrame)
    assert len(scan) > 0
    assert 'dst_port' in scan.columns


def test_attacker_brute_force():
    """Test brute force generation."""
    gen = AttackerBehaviorGenerator()
    bf = gen.generate_brute_force('203.0.113.1', '10.0.0.1')
    
    assert isinstance(bf, pd.DataFrame)
    assert len(bf) > 0
    assert 'failed_logins' in bf.columns


def test_network_simulator():
    """Test network simulator."""
    sim = NetworkSimulator()
    
    normal = sim.simulate_normal_network()
    assert isinstance(normal, pd.DataFrame)
    assert len(normal) > 0


def test_network_under_attack():
    """Test simulating network under attack."""
    sim = NetworkSimulator()
    
    under_attack = sim.simulate_network_under_attack()
    assert isinstance(under_attack, pd.DataFrame)
    assert len(under_attack) > 0
