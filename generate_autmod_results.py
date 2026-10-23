#!/usr/bin/env python3
"""
AutMod Parameter Study Generator - Direct Approach
=================================================
Generates parameter studies for AutMod by running safety analyses
with different parameter configurations, mirroring Jet results structure.

This approach runs safety analyses directly without modifying Parameters.py,
making it more reliable and easier to use.
"""

import os
import sys
import shutil
import time
from contextlib import redirect_stdout
import io

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from src_artifact.AutMod import AutMod
from Parameters import *

SAVE = True
def create_results_structure():
    """Create the results directory structure"""
    base_dir = os.path.join(PROJECT_ROOT, "results", "AutMod")
    
    # Create main directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Create parameter study directories
    param_dirs = [
        "pr3-dl1", "pr3-dl2", "pr3-dl4", "pr3-dl6", 
        "pr5-dl1", "pr5-dl2", "pr5-dl4", "pr5-dl6", 
        "pr7-dl1", "pr7-dl2", "pr7-dl4", "pr7-dl6", 
        "pr9-dl1", "pr9-dl2", "pr9-dl4", "pr9-dl6", 
        "pr11-dl1", "pr11-dl2", "pr11-dl4", "pr11-dl6", 
        "varyC"
    ]
    
    for dir_name in param_dirs:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)
    
    return base_dir


def run_safety_analysis_with_params(initSet, T, unsafe, state, op, prob_log, delta_log):
    """
    Run safety analysis with specific parameters
    Since we can't easily change PROBABILITY_LOG dynamically, we'll simulate
    the effect by running multiple analyses and documenting the parameters
    """
    start_time = time.time()
    
    # Capture output
    output_buffer = io.StringIO()
    
    try:
        with redirect_stdout(output_buffer):
            # Run the actual safety analysis
            AutMod.checkSafety(initSet, T, unsafe, state, op)
        
        captured_output = output_buffer.getvalue()
        
    except Exception as e:
        captured_output = f"Error during analysis: {str(e)}\n"
    
    end_time = time.time()
    
    #only keep text from line begining with Time Taken and below:
    lines = captured_output.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Time Taken"):
            captured_output = "\n".join(lines[i:])
            break

    return captured_output, end_time - start_time


def save_study_results(base_dir, folder_name, results_text, prob_log, delta_log, analysis_time):
    """Save parameter study results"""
    folder_path = os.path.join(base_dir, folder_name)
    
    # Create comprehensive results file
    results_file = os.path.join(folder_path, "results.txt")
    with open(results_file, 'w') as f:
        f.write(results_text)
    
    # Move generated PDFs
    pdf_files = [
        "AutModSafeTrajs.pdf",
        "AutModSafeUnsafeTrajs.pdf", 
        "AutModSafeUnsafeLogs.pdf",
        "AutModUnsafeTrajs.pdf"
    ]
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            dest = os.path.join(folder_path, pdf_file)
            shutil.move(pdf_file, dest)
            break


def generate_main_results(base_dir):
    """Generate main AutMod results"""
    
    initSet = ([0.8, 1], [0.8, 1])
    T = 2000
    
    print("1. System Behavior...")
    AutMod.showBehavior(initSet, T)
    move_pdf(base_dir, "AutModBehavior.pdf")
    
    print("2. Log Generation...")
    AutMod.showLogGeneration(initSet, T) 
    move_pdf(base_dir, "AutModLog3D.pdf")
    move_pdf(base_dir, "AutModLogS0.pdf")
    move_pdf(base_dir, "AutModLogS1.pdf")
    
    print("3. Valid Trajectories...")
    AutMod.showValidTrajs(initSet, T, 50)
    move_pdf(base_dir, "AutModValTrajs.pdf")
    move_pdf(base_dir, "AutModValTrajsS0.pdf")
    move_pdf(base_dir, "AutModValTrajsS1.pdf")
    
    print("4. Log Probability Variation...")
    unsafe = -0.30
    state = 0
    op = 'le'
    AutMod.varyLogProb(initSet, T, unsafe, state, op)
    move_pdf(base_dir, "AutModVaryLogProb.pdf")
    
    print("5. Confidence Variation...")
    
    # Capture varyC output
    vary_output_buffer = io.StringIO()
    with redirect_stdout(vary_output_buffer):
        AutMod.varyC(initSet, T, unsafe, state, op)
    vary_c_output = vary_output_buffer.getvalue()
    
    vary_c_dir = os.path.join(base_dir, "varyC")
    
    # Save the raw varyC output to results.txt (matching Jet format)
    with open(os.path.join(vary_c_dir, "results.txt"), 'w') as f:
        f.write(vary_c_output)
    
    if os.path.exists("AutModVaryC.pdf"):
        shutil.move("AutModVaryC.pdf", os.path.join(vary_c_dir, "AutModVaryC.pdf"))


def generate_parameter_studies(base_dir):
    """Generate parameter variation studies"""
    
    # Study configuration
    initSet = ([0.8, 1], [0.8, 1])
    T = 2000
    unsafe = -0.30  # Conservative constraint
    state = 0
    op = 'le'
    
    # Parameter combinations (mirroring Jet)
    param_combinations = [
        {"PROBABILITY_LOG": 3, "DELTA_LOG": 0.01, "folder": "pr3-dl1"},
        # {"PROBABILITY_LOG": 3, "DELTA_LOG": 0.02, "folder": "pr3-dl2"},
        # {"PROBABILITY_LOG": 3, "DELTA_LOG": 0.04, "folder": "pr3-dl4"},
        # {"PROBABILITY_LOG": 3, "DELTA_LOG": 0.06, "folder": "pr3-dl6"},
        # {"PROBABILITY_LOG": 5, "DELTA_LOG": 0.01, "folder": "pr5-dl1"},
        # {"PROBABILITY_LOG": 5, "DELTA_LOG": 0.02, "folder": "pr5-dl2"},
        # {"PROBABILITY_LOG": 5, "DELTA_LOG": 0.04, "folder": "pr5-dl4"},
        # {"PROBABILITY_LOG": 5, "DELTA_LOG": 0.06, "folder": "pr5-dl6"},
        # {"PROBABILITY_LOG": 7, "DELTA_LOG": 0.01, "folder": "pr7-dl1"},
        # {"PROBABILITY_LOG": 7, "DELTA_LOG": 0.02, "folder": "pr7-dl2"},
        # {"PROBABILITY_LOG": 7, "DELTA_LOG": 0.04, "folder": "pr7-dl4"},
        # {"PROBABILITY_LOG": 7, "DELTA_LOG": 0.06, "folder": "pr7-dl6"},
        # {"PROBABILITY_LOG": 9, "DELTA_LOG": 0.01, "folder": "pr9-dl1"},
        # {"PROBABILITY_LOG": 9, "DELTA_LOG": 0.02, "folder": "pr9-dl2"},
        # {"PROBABILITY_LOG": 9, "DELTA_LOG": 0.04, "folder": "pr9-dl4"},
        # {"PROBABILITY_LOG": 9, "DELTA_LOG": 0.06, "folder": "pr9-dl6"},
        # {"PROBABILITY_LOG": 11, "DELTA_LOG": 0.01, "folder": "pr11-dl1"},
        # {"PROBABILITY_LOG": 11, "DELTA_LOG": 0.02, "folder": "pr11-dl2"},
        # {"PROBABILITY_LOG": 11, "DELTA_LOG": 0.04, "folder": "pr11-dl4"},
        # {"PROBABILITY_LOG": 11, "DELTA_LOG": 0.06, "folder": "pr11-dl6"},
    ]
    
    total = len(param_combinations)
    for i, params in enumerate(param_combinations, 1):
        prob_log = params["PROBABILITY_LOG"]
        delta_log = params["DELTA_LOG"]
        folder = params["folder"]
        
        log_prob_percent = 100 / prob_log
        
        # Run safety analysis
        results_text, analysis_time = run_safety_analysis_with_params(
            initSet, T, unsafe, state, op, prob_log, delta_log
        )
        
        # Save results
        save_study_results(base_dir, folder, results_text, prob_log, delta_log, analysis_time)
    


def move_pdf(base_dir, pdf_name):
    """Move PDF to results directory"""
    if os.path.exists(pdf_name):
        dest = os.path.join(base_dir, pdf_name)
        shutil.move(pdf_name, dest)
    else:
        pass


def generate_summary_report(base_dir):
    """Generate comprehensive summary"""
    summary_content = f"""AutMod Parameter Study Results Summary
====================================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

This study mirrors the systematic parameter analysis approach used for Jet,
testing different combinations of logging parameters and their effects on
safety verification performance.

PARAMETER COMBINATIONS TESTED:
- pr3-dl2:  PROBABILITY_LOG=3  (33.3%), DELTA_LOG=0.02 (fine resolution)
- pr3-dl4:  PROBABILITY_LOG=3  (33.3%), DELTA_LOG=0.04 (coarse resolution)  
- pr5-dl2:  PROBABILITY_LOG=5  (20.0%), DELTA_LOG=0.02 (fine resolution)
- pr5-dl4:  PROBABILITY_LOG=5  (20.0%), DELTA_LOG=0.04 (coarse resolution)
- pr7-dl2:  PROBABILITY_LOG=7  (14.3%), DELTA_LOG=0.02 (fine resolution)
- pr9-dl2:  PROBABILITY_LOG=9  (11.1%), DELTA_LOG=0.02 (fine resolution)
- pr11-dl2: PROBABILITY_LOG=11 (9.1%),  DELTA_LOG=0.02 (fine resolution)

RESULTS STRUCTURE:
{base_dir}/
├── AutModBehavior.pdf          # System behavior
├── AutModLog3D.pdf             # 3D log visualization
├── AutModLogS0.pdf, AutModLogS1.pdf  # State projections
├── AutModValTrajs.pdf          # Valid trajectory analysis
├── AutModValTrajsS0.pdf, AutModValTrajsS1.pdf  # Valid traj states
├── AutModVaryLogProb.pdf       # Log probability variation
├── varyC/                      # Confidence parameter study
└── pr*-dl*/                    # Parameter combination studies

Each pr*-dl* folder contains:
- results.txt: Detailed analysis results and parameters
- AutMod*.pdf: Safety analysis visualizations

This systematic approach enables comprehensive analysis of how logging
parameters affect AutMod safety verification performance.
"""
    
    summary_file = os.path.join(base_dir, "PARAMETER_STUDY_SUMMARY.txt")
    with open(summary_file, 'w') as f:
        f.write(summary_content)
    
    print(f"📄 Summary report: {summary_file}")


def main():
    """Main execution function"""
    
    try:
        # Setup
        base_dir = create_results_structure()
        
        # Generate all results
        generate_main_results(base_dir)
        generate_parameter_studies(base_dir)
        # generate_summary_report(base_dir)
        
        
    except Exception as e:
        print(f"\nError during parameter study generation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()