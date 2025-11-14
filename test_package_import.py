#!/usr/bin/env python3
"""
Test script to verify package imports work correctly
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import the package
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

def test_imports():
    """Test all package imports."""
    print("Testing package imports...")
    print(f"Python path includes: {parent_dir}")
    print("=" * 60)

    # Test 1: Import package
    print("\n1. Testing main package import...")
    try:
        import shs_nature_analysis as shs
        print(f"   ✓ Package imported successfully")
        print(f"   Version: {shs.__version__}")
    except Exception as e:
        print(f"   ✗ Failed to import package: {e}")
        return False

    # Test 2: Check run_pipeline function
    print("\n2. Testing run_pipeline function...")
    try:
        assert hasattr(shs, 'run_pipeline'), "run_pipeline not found"
        print(f"   ✓ run_pipeline function available")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    # Test 3: Import main pipeline class
    print("\n3. Testing SHSAnalysisPipeline import...")
    try:
        from shs_nature_analysis import SHSAnalysisPipeline
        print(f"   ✓ SHSAnalysisPipeline imported successfully")
    except Exception as e:
        print(f"   ✗ Failed to import SHSAnalysisPipeline: {e}")
        return False

    # Test 4: Import submodules
    print("\n4. Testing submodule imports...")
    submodules = ['config', 'data_loader', 'vulnerability', 'financial', 'visualization']
    for module in submodules:
        try:
            mod = getattr(shs, module)
            print(f"   ✓ {module} module accessible")
        except Exception as e:
            print(f"   ✗ Failed to access {module}: {e}")
            return False

    # Test 5: Check config values
    print("\n5. Testing config access...")
    try:
        from shs_nature_analysis import config
        print(f"   ✓ RISK_FREE_RATE: {config.RISK_FREE_RATE}")
        print(f"   ✓ PD_CALIB: {config.PD_CALIB}")
        print(f"   ✓ LGD_CALIB: {config.LGD_CALIB}")
    except Exception as e:
        print(f"   ✗ Failed to access config: {e}")
        return False

    # Test 6: Check financial functions
    print("\n6. Testing financial functions...")
    try:
        from shs_nature_analysis import financial
        assert hasattr(financial, 'pd_to_dd'), "pd_to_dd not found"
        assert hasattr(financial, 'dd_to_pd'), "dd_to_pd not found"
        assert hasattr(financial, 'calculate_asset_volatility'), "calculate_asset_volatility not found"
        print(f"   ✓ Financial functions accessible")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    # Test 7: Test a simple calculation
    print("\n7. Testing a simple calculation...")
    try:
        from shs_nature_analysis import financial
        pd_value = 0.05
        dd = financial.pd_to_dd(pd_value)
        pd_back = financial.dd_to_pd(dd)
        assert abs(pd_value - pd_back) < 1e-10, "Round-trip conversion failed"
        print(f"   ✓ PD={pd_value:.4f} -> DD={dd:.4f} -> PD={pd_back:.4f}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    # Test 8: Check visualization module
    print("\n8. Testing visualization module...")
    try:
        from shs_nature_analysis import visualization
        assert hasattr(visualization, 'create_heatmap'), "create_heatmap not found"
        assert hasattr(visualization, 'plot_loss_heatmap_by_dimension'), "plot_loss_heatmap_by_dimension not found"
        print(f"   ✓ Visualization functions accessible")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    import sys
    success = test_imports()
    sys.exit(0 if success else 1)
