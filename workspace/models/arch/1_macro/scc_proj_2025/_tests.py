import sys
import os
import yaml
import copy
import matplotlib.pyplot

# fmt: off
THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_NAME = os.path.basename(THIS_SCRIPT_DIR)
sys.path.append(os.path.abspath(os.path.join(THIS_SCRIPT_DIR, '..', '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(THIS_SCRIPT_DIR, 'workloads')))
from scripts import utils as utl
import helper_functions
import scripts
# fmt: on


IMPORTANT_COMPONENTS = ['vec_mac', 'A_Reg', 'A_Buffer', 'B_Buffer', 'accumulation_collector', 'ppu', 'output_buffer']

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
        system="fetch_all_lpddr4",
    )

    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

def test_sparsemm_energy_breakdown(sparsity=1.0, bitwidth=4):
    """
    ### Matrix Multiply Energy Breakdown 

    This test evaluates the energy breakdown for a matrix multiply workload
    where both input matrix A and weight matrix B are drawn from a Gaussian
    distribution with inputted sparsity.
    
    Parameters:
        sparsity (float) (optional): decimal sparsity amount, 0.5 == 50% sparsity.
                                     Currently has no impact on simulation
        bitwdith (int) (optional): size of input bits, if you're using INT4/INT4-VSQ or INT8
    """

    results = utl.run_layer(
        macro=MACRO_NAME,
        layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
        variables=dict(
            INPUT_BITS=bitwidth,
            WEIGHT_BITS=bitwidth,
            OUTPUT_BITS=bitwidth,
            sparsity=sparsity
        ),
        system="fetch_all_lpddr4",
    )

    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

# def test_idle_energy_breakdown(sparsity, bitwidth):
#     """
#     ### Matrix Multiply Energy Breakdown 

#     This test evaluates the energy breakdown for a matrix multiply workload
#     where both input matrix A and weight matrix B are drawn from a Gaussian
#     distribution with inputted sparsity.
    
#     Possible Parameters for future:
#         bitwdith (int) (optional): size of input bits, if you're using INT4/INT4-VSQ or INT8
#         sparsity (float) (optional): decimal sparsity amount, 0.5 == 50% sparsity
#         std (float) (optional): standard deviationi for Gaussian distribution
#     """

#     results = utl.run_layer(
#         macro=MACRO_NAME,
#         layer="arch/1_macro/scc_proj_2025/workloads/all_zeros.yaml",
#         variables=dict(
#             INPUT_BITS=bitwidth,
#             WEIGHT_BITS=bitwidth,
#             OUTPUT_BITS=bitwidth,
#             sparsity=sparsity
#         ),
#         system="fetch_all_lpddr4",
#     )

#     results.clear_zero_areas()
#     results.clear_zero_energies()
#     return results


# def sweep_sparsities(bitwidth=4, technology='5nm'):
#     """
#     ### Sparsity Sweep

#     This test sweeps through a set of matrix sparities and plots the 
#     """
#     n = 20
#     ops = 8192 * 16 * 16 * 2

#     sparsities = list(i/n for i in range(0, n + 1))
#     energies = []
    
#     for sparsity in sparsities:
#         results = utl.run_layer(
#             macro=MACRO_NAME,
#             layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
#             variables=dict(
#                 INPUT_BITS=bitwidth,
#                 WEIGHT_BITS=bitwidth,
#                 OUTPUT_BITS=bitwidth,
#                 sparsity=sparsity/n,
#                 TECHNOLOGY=technology
#             ),
#             system="fetch_all_lpddr4",
#         )
    
#         results.clear_zero_areas()
#         results.clear_zero_energies()

#         energies.append(sum(results.percomponent
        
#     return results


if __name__ == "__main__":
    test_area_energy_breakdown()