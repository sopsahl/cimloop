import sys
import os
import yaml
import copy

# fmt: off
THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_NAME = os.path.basename(THIS_SCRIPT_DIR)
sys.path.append(os.path.abspath(os.path.join(THIS_SCRIPT_DIR, '..', '..', '..', '..')))
from scripts import utils as utl
import helper_functions
import scripts
# fmt: on

def test_area_energy_breakdown():
    """
    ### Area and energy breakdown
    This example architecture doesn't have a suite of tests, but you may
    look at the other example architectures for inspiration.        
    """
    results = utl.single_test(utl.quick_run(macro=MACRO_NAME))

    results = utl.parallel_test(
        utl.delayed(utl.quick_run)(
            macro=MACRO_NAME,
            variables=dict(
                QUANTIZE=q,
            ),
        )
        for q in [False, True]
    )
    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

def test_mm_energy_breakdown():
    """
    ### Matrix Multiply Energy Breakdown 

    This test evaluates the energy breakdown for a matrix multiply workload
    where both input matrix A and weight matrix B are drawn from a Gaussian
    distribution with inputted sparsity.
    
    Possible Parameters for future:
        bitwdith (int) (optional): size of input bits, if you're using INT4/INT4-VSQ or INT8
        sparsity (float) (optional): decimal sparsity amount, 0.5 == 50% sparsity
        std (float) (optional): standard deviationi for Gaussian distribution
    """

    results = utl.run_layer(
        macro=MACRO_NAME,
        layer="simple_matmul",
        variables=dict(
            INPUT_BITS=4,
            WEIGHT_BITS=4,
            OUTPUT_BITS=4,
        ),
    )

    results.clear_zero_areas()
    results.clear_zero_energies()
    return results


if __name__ == "__main__":
    test_area_energy_breakdown()