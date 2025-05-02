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


IMPORTANT_COMPONENTS = ['mac8', 'mac4', 'mac4_vsq', 'A_Reg', 'A_Buffer', 'B_Buffer', 'accumulation_collector', 'ppu', 'output_buffer']


def test_mm_energy_breakdown(sparsity=1.0, bitwidth=4, voltage=0.67):
    """

    """

    results = utl.run_layer(
        macro=MACRO_NAME,
        layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
        variables=dict(
            INPUT_BITS=bitwidth,
            WEIGHT_BITS=bitwidth,
            OUTPUT_BITS=bitwidth,
            PRECISION=bitwidth,
            sparsity=sparsity
        ),
        system="fetch_all_lpddr4",
    )

    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

def sweep_voltages(precision=4):
    """

    """
    topsw = []
    voltages = [0.67, 0.46, 0.5, 0.55, 0.60, 0.75, 0.85, 0.95, 1.05]
    for voltage in voltages:
        
        results = utl.run_layer(
            macro=MACRO_NAME,
            layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
            variables=dict(
                INPUT_BITS=precision,
                WEIGHT_BITS=precision,
                OUTPUT_BITS=precision,
                VOLTAGE=voltage
            ),
            system="fetch_all_lpddr4",
        )
    
        results.clear_zero_areas()
        results.clear_zero_energies()
        energies = results.per_component_energy
        computes = results.computes
        latency = results.latency

        total_energy = sum(energy for comp, energy in energies.items() if comp in IMPORTANT_COMPONENTS)
        
        topsw.append(2 * computes / total_energy / 1e12)

    return topsw, voltages

def test_datapath():
    """

    """
    
    results = utl.run_layer(
        macro=MACRO_NAME,
        layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
        variables=dict(
            INPUT_BITS=4,
            WEIGHT_BITS=4,
            OUTPUT_BITS=4,
        ),
        system="fetch_all_lpddr4",
    )

    results.clear_zero_areas()
    results.clear_zero_energies()
    energies = results.per_component_energy
    computes = results.computes
    latency = results.latency

    total_energy = sum(energy for comp, energy in energies.items() if comp in IMPORTANT_COMPONENTS)
    
    topsw = (2 * computes / total_energy / 1e12)

    return topsw



def sweep_technologies(precision=4):
    """
   
    """ 
    topsw = []
    technologies = [5, 7, 10, 22, 28, 40, 65]
    areas = []
    for technology in technologies:
        
        results = utl.run_layer(
            macro=MACRO_NAME,
            layer="arch/1_macro/scc_proj_2025/workloads/sparsemm.yaml",
            variables=dict(
                INPUT_BITS=precision,
                WEIGHT_BITS=precision,
                OUTPUT_BITS=precision,
                TECHNOLOGY=technology
            ),
            system="fetch_all_lpddr4",
        )
    
        results.clear_zero_areas()
        results.clear_zero_energies()

        total_energy = sum(energy for comp, energy in results.per_component_energy.items() if comp in IMPORTANT_COMPONENTS)
        total_area = sum(area for comp, area in results.per_component_area.items() if comp in IMPORTANT_COMPONENTS)
        topsw.append(2 * results.computes / total_energy / 1e12)
        areas.append(total_area)

    return topsw, areas, technologies
        

        

        

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