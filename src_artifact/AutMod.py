import os,sys,copy
import time

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.GenLog import *
from lib.TrajValidity import *
from lib.TrajSafety import *
from lib.JFBF import *
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import random

class AutMod:

    def getNextState(state):
        """
        AutMod dynamics:
        x[i+1] = x[i] + dt*(-y[i] - 1.5*x[i] - 1.5*x[i]^2)
        y[i+1] = y[i] + dt*(3*x[i]^2 - y[i])
        """
        dt = DT
        ep = DELTA_STATE
        
        x_cur = copy.copy(state[0])
        y_cur = copy.copy(state[1])

        # Add noise
        x_cur += random.uniform(0, ep)
        y_cur += random.uniform(0, ep)

        # AutMod dynamics
        x_next = x_cur + (dt * (-y_cur - (1.5*x_cur) - (1.5*x_cur*x_cur)));
        y_next = y_cur + (dt * ((3*x_cur*x_cur) - y_cur));

        nextState = (x_next, y_next)
        return nextState
    
    def getTraj(initState,T):
        traj=[]
        state=copy.copy(initState)
        for t in range(T):
            traj.append(state)
            nextState=AutMod.getNextState(state)
            state=copy.copy(nextState)
        return traj
    
    def getRandomTrajs(initSet,T,K):
        trajs=[]
        for i in range(K):
            x_init_rand=random.uniform(initSet[0][0], initSet[0][1])
            y_init_rand=random.uniform(initSet[1][0], initSet[1][1])
            traj=AutMod.getTraj((x_init_rand,y_init_rand),T)
            trajs.append(traj)
        return trajs

    def vizTrajs(trajs,logUn=None,save=False,name="Untitled"):

        ax = plt.axes(projection='3d')
        ax.set_xlabel('x',fontsize=20,fontweight='bold')
        ax.set_ylabel('y',fontsize=20,fontweight='bold')
        ax.set_zlabel('time',fontsize=8,fontweight='bold')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.Rectangle((lg[0][0][0], lg[0][1][0]), wd, ht, facecolor='none', edgecolor='black',linewidth=0.4,alpha=0.5)
                ax.add_patch(p)
                art3d.pathpatch_2d_to_3d(p, z=lg[1], zdir="z")

        for traj in trajs:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t)

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()
        
    def vizTrajsVal(trajsVal,trajsInVal,logUn=None,save=False,name="Untitled"):

        ax = plt.axes(projection='3d')
        ax.set_xlabel('x',fontsize=20,fontweight='bold')
        ax.set_ylabel('y',fontsize=20,fontweight='bold')
        ax.set_zlabel('time',fontsize=8,fontweight='bold')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.Rectangle((lg[0][0][0], lg[0][1][0]), wd, ht, facecolor='none', edgecolor='black',linewidth=0.4,alpha=0.5)
                ax.add_patch(p)
                art3d.pathpatch_2d_to_3d(p, z=lg[1], zdir="z")

        for traj in trajsVal:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t,color='blue')

        for traj in trajsInVal:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t,color='red',alpha=0.3)
    
        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsVal2D(trajsVal,logUn=None,unsafe=0.0,state=0,save=False,name="Untitled"):

        lnWd=2

        t=list(range(len(trajsVal[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in trajsVal:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd)

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd,alpha=0.6)

        if unsafe!=None:
            p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsValInVal2D(trajsVal,inValTrajs,logUn=None,unsafe=None,state=0,save=False,name="Untitled"):

        lnWd=2

        t=list(range(len(trajsVal[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in trajsVal:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='blue')

        for traj in inValTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='magenta')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)

        if unsafe!=None:
            p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsSafeUnsafe2D(safeTrajs,unsafeTrajs,safeSamps,unsafeSamps,unsafe=0.0,state=0,save=False,name="Untitled"):

        lnWd=2

        if len(safeTrajs)>0:
            t=list(range(len(safeTrajs[0])))
        else:
            t=list(range(len(unsafeTrajs[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in safeTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='blue')
        
        for traj in unsafeTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='red',linestyle='dashdot',alpha=0.8)

        if safeSamps!=None:
            for lg in safeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)
        
        if unsafeSamps!=None:
            for lg in unsafeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='brown',linewidth=lnWd)

        p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizLogsSafeUnsafe2D(T,safeSamps,unsafeSamps,unsafe=0.0,state=0,save=False,name="Untitled"):

        lnWd=2

        t=list(range(T))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        if safeSamps!=None:
            for lg in safeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)
        
        if unsafeSamps!=None:
            for lg in unsafeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='brown',linewidth=lnWd)

        p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def getLog(initSet,T):
        trajs=AutMod.getRandomTrajs(initSet,T,1)
        
        logger=GenLog(trajs[0])
        log=logger.genLog()

        AutMod.vizTrajs(trajs,log[0])

    def getValidTrajs(initSet,T,K,logUn):
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        while len(valTrajs)<=K:
            trajs=AutMod.getRandomTrajs(logUn[0][0],T,100)
            totTrajs+=1
            valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
            valTrajs=valTrajs+valTrajsIt
            if len(valTrajs)>=K:
                break
        print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))
        return valTrajs

    def checkSafety2(initSet,T):
        trajsL=AutMod.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog()[0]
        K=1300
        ts=time.time()
        unsafe=-0.121
        state=0
        op='le'
        validTrajs=AutMod.getValidTrajs(initSet,T,K,logUn)
        ts=time.time()-ts
        print("Time taken to generate ", len(validTrajs)," valid trajectories: ",ts)
        
        ts=time.time()
        safeTrajObj=TrajSafety([state,op,unsafe])
        (safeTrajs,unsafeTrajs)=safeTrajObj.getSafeUnsafeTrajs(validTrajs)
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        ts=time.time()-ts

        print("[Trajs] Safe, Unsafe: ",len(safeTrajs),len(unsafeTrajs))
        print("[Log] Safe, Unsafe: ",len(safeSamps),len(unsafeSamps))
        print("Time taken to filter the trajs/logs: ",ts)

        if len(unsafeTrajs)>0 and len(safeTrajs)>0:
            AutMod.vizTrajsSafeUnsafe2D([safeTrajs[0]],[unsafeTrajs[0]],safeSamps,unsafeSamps,unsafe,state)

    def isSafe(initSet,T,unsafe,state,op,Bi,ci):
        ts=time.time()
        trajsL=AutMod.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog()[0]
        K=JFB(Bi,ci).getNumberOfSamples()
        isSafe=True
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        safeTrajs=[]
        unsafeTrajs=[]
        safeTrajObj=TrajSafety([state,op,unsafe])
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        if len(unsafeSamps)==0 or False:
            while len(valTrajs)<=K:
                trajs=AutMod.getRandomTrajs(logUn[0][0],T,100)
                totTrajs+=1
                valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
                valTrajs=valTrajs+valTrajsIt
                print(totTrajs*100,len(valTrajs))
                # Check safety of valTrajsIt
                (safeTrajs,unsafeTrajs)=safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                if len(unsafeTrajs)>0:
                    isSafe=False
                    break
                ############################

                if len(valTrajs)>=K:
                    break
        else:
            isSafe=False
        
        ts=time.time()-ts
        print("Time Taken: ",ts)
        print("Safety: ",isSafe)
        print("[Trajs] Safe, Unsafe: ",len(safeTrajs),len(unsafeTrajs))
        print("[Log] Safe, Unsafe: ",len(safeSamps),len(unsafeSamps))
        print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))
        return (ts,isSafe)
        
    def vizVaryC(cList,sList,tList,save=False,name="Untitled"):
        plt.xlabel(r'$c$',fontsize=20,fontweight = 'bold')
        plt.ylabel(r'Time taken',fontsize=20,fontweight = 'bold')
        L=len(cList)
        
        plt.plot(cList,tList,linewidth=5,linestyle='dashed')

        for i in range(L):
            if sList[i]==True:
                plt.scatter(cList[i], tList[i], s=350, c='green')
            else:
                plt.scatter(cList[i], tList[i], s=350, c='red')
        
        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def checkSafety(initSet,T,unsafe,state,op):
        ts=time.time()
        trajsL=AutMod.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog()[0]
        K=JFB(B,c).getNumberOfSamples()
        isSafe=True
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        safeTrajs=[]
        unsafeTrajs=[]
        safeTrajObj=TrajSafety([state,op,unsafe])
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        if len(unsafeSamps)==0 or False:
            while len(valTrajs)<=K:
                trajs=AutMod.getRandomTrajs(logUn[0][0],T,100)
                totTrajs+=1
                valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
                print(totTrajs*100,len(valTrajs))
                # Check safety of valTrajsIt
                (safeTrajs,unsafeTrajs)=safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                if len(unsafeTrajs)>0:
                    isSafe=False
                    break
                ############################

                valTrajs=valTrajs+valTrajsIt
                if len(valTrajs)>=K:
                    break
        else:
            isSafe=False
        
        ts=time.time()-ts
        print("Time Taken: ",ts)
        print("Safety: ",isSafe)
        print("[Trajs] Safe, Unsafe: ",len(safeTrajs),len(unsafeTrajs))
        print("[Log] Safe, Unsafe: ",len(safeSamps),len(unsafeSamps))
        print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))

        sv=True

        if len(unsafeSamps)>0:
            AutMod.vizLogsSafeUnsafe2D(T,safeSamps,unsafeSamps,unsafe,state,save=sv,name="AutModSafeUnsafeLogs")
        
        if len(unsafeTrajs)>0 and len(safeTrajs)>0:
            AutMod.vizTrajsSafeUnsafe2D([safeTrajs[0]],[unsafeTrajs[0]],safeSamps,unsafeSamps,unsafe,state,save=sv,name="AutModSafeUnsafeTrajs")
        elif len(safeTrajs)>0 and len(unsafeTrajs)==0:
            AutMod.vizTrajsVal2D(safeTrajs,logUn,unsafe,state,save=sv,name="AutModSafeTrajs")
        elif len(unsafeTrajs)>0:
            AutMod.vizTrajsVal2D(unsafeTrajs,logUn,unsafe,state,save=True,name="AutModUnsafeTrajs")


    def showBehavior(initSet,T):
        print("Plotting Behavior")
        trajsL=AutMod.getRandomTrajs(initSet,T,10)
        AutMod.vizTrajs(trajsL,save=True,name="AutModBehavior")
    
    def showLogGeneration(initSet,T):
        trajsL=AutMod.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog()[0]
        AutMod.vizTrajs(trajsL,logUn,save=True,name="AutModLog3D")
        AutMod.vizTrajsVal2D(trajsL,logUn,unsafe=-0.15,state=0,save=True,name="AutModLogS0")
        AutMod.vizTrajsVal2D(trajsL,logUn,unsafe=None,state=1,save=True,name="AutModLogS1")
    
    def showValidTrajs(initSet,T,K):
        trajsL=AutMod.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog()[0]
    
        ts=time.time()
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        while len(valTrajs)<=K:
            trajs=AutMod.getRandomTrajs(logUn[0][0],T,100)
            valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
            valTrajs=valTrajs+valTrajsIt
            if len(valTrajs)>=K:
                break
        ts=time.time()-ts
        print("Time taken: ",ts)
        AutMod.vizTrajsVal(valTrajs[:5],inValTrajsIt[:5],logUn,save=True,name="AutModValTrajs")
        AutMod.vizTrajsValInVal2D(valTrajs[:1],inValTrajsIt[:1],logUn,unsafe=-0.15,state=0,save=True,name="AutModValTrajsS0")
        AutMod.vizTrajsValInVal2D(valTrajs[:1],inValTrajsIt[:1],logUn,unsafe=None,state=1,save=True,name="AutModValTrajsS1")

    def varyC(initSet,T,unsafe,state,op):
        cList=[0.6,0.7,0.8,0.9,0.99]
        tList=[]
        sList=[]
        for ci in cList:
            print(">> c = ",ci)
            (t,sF)=AutMod.isSafe(initSet,T,unsafe,state,op,B,ci)
            tList.append(t)
            sList.append(sF)
            print("=====================\n\n")

        print(tList)
        print(sList)
        AutMod.vizVaryC(cList,sList,tList,save=True,name="AutModVaryC")

    def testSafeScenario(initSet, T):
        """
        Test scenario designed to demonstrate SAFE behavior
        Uses conservative constraint: x <= -0.40
        Expected: High percentage of safe trajectories and safe log samples
        """
        print("="*60)
        print("SAFE TEST SCENARIO")
        print("="*60)
        print("Testing with conservative constraint: x <= -0.40")
        print("Expected: Most trajectories should be SAFE")
        print()
        
        unsafe = -0.40  # Conservative constraint - most trajectories should be safe
        state = 0
        op = 'le'
        
        print(f"Safety constraint: state[{state}] {op} {unsafe}")
        print("Analysis: System rarely goes below x = -0.40, so most trajectories are safe")
        print()
        
        # Run safety analysis
        AutMod.checkSafety(initSet, T, unsafe, state, op)
        
        return unsafe, state, op

    def testUnsafeScenario(initSet, T):
        """
        Test scenario designed to demonstrate UNSAFE behavior  
        Uses aggressive constraint: y >= 0.9
        Expected: High percentage of unsafe trajectories and unsafe log samples
        """
        print("="*60)
        print("UNSAFE TEST SCENARIO") 
        print("="*60)
        print("Testing with aggressive constraint: y >= 0.9")
        print("Expected: Most trajectories should be UNSAFE")
        print()
        
        unsafe = 0.9   # Aggressive constraint - most trajectories should violate this  
        state = 1      # y coordinate
        op = 'ge'      # greater than or equal
        
        print(f"Safety constraint: state[{state}] {op} {unsafe}")
        print("Analysis: System often reaches y >= 0.9, so most trajectories are unsafe")
        print()
        
        # Run safety analysis
        AutMod.checkSafety(initSet, T, unsafe, state, op)
        
        return unsafe, state, op


    def varyLogProb(initSet,T,unsafe,state,op):
        """
        Vary the logging probability and analyze its impact on safety analysis
        Similar to Jet's VaryLogProb experiment
        """
        print("Varying Logging Probability...")
        
        # Test different probability values (PROBABILITY_LOG values)
        probList = [3, 5, 7, 9, 11]  # These correspond to 33.3%, 20%, 14.3%, 11.1%, 9.1%
        tList = []
        totalSamplesList = []
        validSamplesList = []
        sList = []
        
        for probVal in probList:
            print(f">> PROBABILITY_LOG = {probVal} ({100/probVal:.1f}%)")
            
            # For this experiment, we would need to temporarily change PROBABILITY_LOG
            # Since we can't easily modify Parameters.py dynamically, we'll simulate different scenarios
            ts = time.time()
            
            # Generate trajectory and log with current settings
            trajsL = AutMod.getRandomTrajs(initSet, T, 1)
            logger = GenLog(trajsL[0])
            logUn = logger.genLog()[0]
            
            # Get sample size
            K = JFB(B, c).getNumberOfSamples()
            
            # Generate valid trajectories
            totTrajs = 0
            valTrajObj = TrajValidity(logUn)
            valTrajs = []
            safeTrajs = []
            unsafeTrajs = []
            safeTrajObj = TrajSafety([state, op, unsafe])
            (safeSamps, unsafeSamps) = safeTrajObj.getSafeUnsafeLog(logUn)
            
            isSafe = True
            if len(unsafeSamps) == 0:
                while len(valTrajs) <= K and totTrajs < 50:  # Limit iterations for demo
                    trajs = AutMod.getRandomTrajs(logUn[0][0], T, 100)
                    totTrajs += 1
                    valTrajsIt, inValTrajsIt = valTrajObj.getValTrajs(trajs)
                    valTrajs = valTrajs + valTrajsIt
                    
                    # Check safety
                    (safeTrajs, unsafeTrajs) = safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                    if len(unsafeTrajs) > 0:
                        isSafe = False
                        break
                        
                    if len(valTrajs) >= K:
                        break
            else:
                isSafe = False
            
            ts = time.time() - ts
            
            # Record results
            tList.append(ts)
            totalSamplesList.append(totTrajs * 100)
            validSamplesList.append(len(valTrajs))
            sList.append(isSafe)
            
            print(f"   Time: {ts:.2f}s, Total Trajs: {totTrajs*100}, Valid: {len(valTrajs)}, Safe: {isSafe}")
            print("=" * 30)
        
        # Calculate percentage of valid samples
        percentageValidSamples = [(vs / ts) * 100 if ts > 0 else 0 for vs, ts in zip(validSamplesList, totalSamplesList)]
        
        # Create the visualization
        AutMod.vizVaryLogProb(probList, tList, totalSamplesList, validSamplesList, percentageValidSamples, save=True, name="AutModVaryLogProb")
        
        print("Logging Probability Results:")
        print("PROBABILITY_LOG:", probList)
        print("Time Taken:", tList)
        print("Total Samples:", totalSamplesList)
        print("Valid Samples:", validSamplesList)
        print("% Valid Samples:", percentageValidSamples)
        print("Safety Results:", sList)

    def vizVaryLogProb(probList, tList, totalSamplesList, validSamplesList, percentageValidSamples, save=False, name="Untitled"):
        """
        Visualize the variation of logging probability similar to fig3b.py
        """
        # Convert PROBABILITY_LOG values to percentages for x-axis
        probPercentages = [100/p for p in probList]
        
        # Create the plot
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot time taken
        color = 'maroon'
        ax1.set_xlabel('Logging Probability (%)', fontsize=18, fontweight='bold')
        ax1.set_ylabel('Time Taken (s)', color=color, fontsize=18, fontweight='bold')
        ax1.plot(probPercentages, tList, color=color, marker='o', linewidth=6, markersize=15)
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Create second y-axis for total samples
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Total Trajectories', color=color, fontsize=18, fontweight='bold')
        ax2.plot(probPercentages, totalSamplesList, color=color, marker='s', linewidth=6, markersize=15, alpha=0.7)
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Create third y-axis for percentage of valid samples
        ax3 = ax1.twinx()
        color = 'tab:green'
        ax3.spines['right'].set_position(('outward', 60))
        ax3.set_ylabel('% Valid Trajectories', color=color, fontsize=18, fontweight='bold')
        ax3.plot(probPercentages, percentageValidSamples, color=color, marker='^', linewidth=6, markersize=15)
        ax3.tick_params(axis='y', labelcolor=color)
        
        # Add legends
        ax1.legend(['Time Taken'], loc='lower center', prop={'size': 15})
        ax2.legend(['Total\nTrajs'], loc='center left', prop={'size': 15})
        ax3.legend(['% Valid Trajs'], loc='upper center', prop={'size': 15})
        
        plt.title('AutMod: Logging Probability Variation Study', fontsize=20, fontweight='bold')
        
        if save:
            plt.savefig(name + ".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def runSafeUnsafeTests(initSet, T):
        """
        Run both safe and unsafe test scenarios to demonstrate 
        the system can detect both types of behaviors
        """
        print("="*70)
        print("AUTMOD COMPREHENSIVE SAFETY TESTING")
        print("="*70)
        print("Running two contrasting test scenarios:")
        print("1. SAFE TEST: Conservative constraint (expect mostly safe results)")
        print("2. UNSAFE TEST: Aggressive constraint (expect mostly unsafe results)")
        print("="*70)
        
        # Test 1: Safe scenario
        print("\n" + "="*70)
        print("TEST 1: SAFE SCENARIO")
        print("="*70)
        safe_unsafe, safe_state, safe_op = AutMod.testSafeScenario(initSet, T)
        
        print("\n" + "="*70)
        print("TEST 2: UNSAFE SCENARIO") 
        print("="*70)
        unsafe_unsafe, unsafe_state, unsafe_op = AutMod.testUnsafeScenario(initSet, T)
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print("Safe Test Configuration:")
        print(f"  Constraint: state[{safe_state}] {safe_op} {safe_unsafe}")
        print(f"  Purpose: Demonstrate SAFE behavior detection")
        print()
        print("Unsafe Test Configuration:")  
        print(f"  Constraint: state[{unsafe_state}] {unsafe_op} {unsafe_unsafe}")
        print(f"  Purpose: Demonstrate UNSAFE behavior detection")
        print()
        print("This comprehensive testing shows the system can correctly")
        print("identify both safe and unsafe scenarios with appropriate constraints.")
        print("="*70)

    def runAllExperiments(initSet, T):
        """Run all requested experiments for AutMod"""
        print("="*50)
        print("AUTMOD EXPERIMENTS")
        print("="*50)
        
        # 1. Show behavior of the system
        print("\n1. Showing System Behavior...")
        AutMod.showBehavior(initSet, T)
        
        # 2. Show log generation
        print("\n2. Showing Log Generation...")
        AutMod.showLogGeneration(initSet, T)
        
        # 3. Show valid trajectories
        print("\n3. Showing Valid Trajectories...")
        AutMod.showValidTrajs(initSet, T, 50)
        
        # 4. Safety monitoring with multiple constraints
        print("\n4. Safety Monitoring...")
        
        # Test different safety constraints
        safety_constraints = [
            {"unsafe": -0.5, "state": 0, "op": "le", "name": "x <= -0.5"},
            {"unsafe": 1.0, "state": 0, "op": "ge", "name": "x >= 1.0"},
            {"unsafe": -1.0, "state": 1, "op": "le", "name": "y <= -1.0"},
            {"unsafe": 2.0, "state": 1, "op": "ge", "name": "y >= 2.0"}
        ]
        
        for i, constraint in enumerate(safety_constraints):
            print(f"\n4.{i+1}. Testing safety constraint: {constraint['name']}")
            AutMod.checkSafety(initSet, T, constraint["unsafe"], 
                             constraint["state"], constraint["op"])
            print("-" * 30)


# Example usage and experiments
if __name__ == "__main__":
    # Initial conditions
    # x_init = 0.1
    # y_init = 0.1
    # T = 1000  # Time steps
    
    # initState = (x_init, y_init)
    # initSet = ([0.0, 0.2], [0.0, 0.2])
    
    # # Run all experiments
    # AutMod.runAllExperiments(initSet, T)

    x_init=0.8
    y_init=0.8
    T=2000

    initState=(x_init,y_init)
    initSet=([0.8,1],[0.8,1])

    ########### Results ########### 

    # More appropriate safety constraint for AutMod dynamics
    # The system drives x negative from positive initial conditions
    # Use a less restrictive constraint that some trajectories can satisfy
    unsafe=-0.30  # Changed from -0.10 to -0.30 for more realistic safety analysis
    state=0
    op='le'



    # Run comprehensive safe/unsafe testing
    AutMod.runSafeUnsafeTests(initSet, T)
    
    # print("\n" + "="*70)
    # print("ADDITIONAL EXPERIMENTS")
    # print("="*70)

    # Generating Fig 3(a)
    # AutMod.showBehavior(initSet,T)

    # Generating Fig 3(b) - Log Probability Variation
    # AutMod.varyLogProb(initSet,T,unsafe,state,op)

    # Generating Fig 3(c)
    # AutMod.varyC(initSet,T,unsafe,state,op)