# PIMPA

**Fabrizio's commit 09/02/2023**

1. I streamlined the examples in a format that can be used with students

2. I added the support for the collateral model with a number of simplifications documented in the PIMPA presentation

3. I removed the documentation (since we will keep it somewhere else) and some legacy files

4. I resolved several bugs. For every change ensure that (at least) the three examples files work

5. I streamlined the data to support the working examples


Fabrizio's commit 22/12/2022

I added support for EQ EUR OPTIONS and for Market Implied time-dependent GBM process. 






Fabrizio's review 10/12/2022

I completed the code review and the trade - portfolio - CCR run comes along very well. No specific concerns (few points below, only 2 may require extra work). We can use our meeting on Monday primarily to agree next steps. 

1. I do not understand the construct in file interest_rate_swap.py line 20-23. I suppose the aim is to add the discount curve as a trade underlying in the case the floating rate is not (a discount curve)?

2. Looking at global parameters calibration_parameters = { 'calibration_method': 'direct_input’}, my understanding is that we have a single choice that is common to ALL models, i.e. we cannot have an hybrid (some models are market implied while some others uses a pre-computed calibration).  We can potentially use a similar structure but having a nested dictionary that distinguishes the different models? This is relevant since in the 2023 course implementation GBM will be ’market_implied’ while HW1F will be ‘direct_input’. 

3. Discussion item: for the EQ implied volatility, I should introduce a Surface object as well. I intend to use a similar template to “Curve” and Interp2d function. 






Fabrizio's review as 02/12/2022 

1. In example notebook 4, what is the meaning of using a RF as name for the pricer, see InterestRateSwapPricer('USD_ZERO_YIELD_CURVE’)? I did not understand which role the attribute "name" plays in the valuation.
> It was a silly shortcut, in order not to change names of market data. I will fix this, it is confusing. 

> OK

> AS 7Dec: Fixed!

2. …simulated_underlying = [rf for rf in underlyings if rf in scenarios] —> the RF is the simulated curve, but the scenario is named by the risk driver, i.e. the short rate (even if you have a single factor model). This is a similar inconsistency to the ones we discussed below (e.g. items 4 and 11 from the last review). 
> My initial thought was to return risk factors, and not risk drivers (so one HW2F curve object instead of the two risk drivers numbers). After our discussion on factor models, I realized that that thought does not cover well the factor modeling. I will think of a couple of different solution here, and discuss that with you. As mentioned, this is the biggest gap in the current design. 

> OK and (while not clear in my comment), I understand this is post version 1 problem. 

3. Class SimulatedData, why we do need an abstract class? I think I get how you use it for HW1F but I am not sure I understand what is use of the general construct. We can discuss it. 
> The idea is actually to have the simulated class come out of RFE simulations (with a translation layer), and query that directly in the pricers. Now the translation is done in the pricer which is not ideal. Do you think this is overengineering?

> OK, now I get it a bit more but at this stage seems over-engineering (I would not see a simple way to explain it to a student). I suggest to defer the design of this kind of logic to the point where we have a clean way to handle the dicotomy risk factors - risk drivers. Since we may use precisely something along the lines of what you have implemented (for example, the representation of rf in a multi-factor model requires a linear composition of the risk drivers).

> AS 7Dec: So while the abstract class is at this stage not necessary, can't we just explain them that this is where we translate from the raw simulated values to the objects which are necessary for the computation (i.e. financial objects like curves). At some point one needs to do this translation. I also do not use the abstract fromulation in the code.

4. I looked at your solution for IRS pricer and it seems consistent with my original code (see separate email). 
> I will check this this weekend.
> AS 7Dec: Checked, and I think now there is a version in it which is easy to understand and correct. I made an error in the previous version. 

5. The notebook 5 does not work for me. The last entry (portfolio.load(global_parameters) / print(portfolio)) gives me an error: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
> Fixed!

>OK



Library for Portfolio Risk Computation

Current Code Status:
READY:
- Risk Factor Evolutions and Notebook 1 Functionality
- Scenario Generation and Notebook 2 Functionality
- Trades and Portfolio Functionality and Notebook 5 Functionality
- Pricers and Notebook 4 Functionality
- CCR Valuation Session and Notebook 6 Functionality

NOT READY:
- Backtesting
- Some RFE


Fabrizio's question based on recent commit:

1. Why file __init__py in every folder?
> They allow relative imorts within a package. So instead of having to work with sys.path, we can simply import other components by dots, e.g. ..utils.calendar 

2. I assume that a kwargs input is treated as a dictionary with string type keys?
> Correct.

3. Should the __str__(self) method for the RFEevolution class be abstract as well (if possible at all)or be a children class method? In its current implementation, it does provide hardly any info.
> Yes, that's one option. An even more elegant way is to implement __str__ in the base class with a default behavior, and then implement __str__ in the child classes with an explicit call to super().__str__ and then adding on top of it. And yes, I have skipped the part of printing info for now, this can be easily added later.

4. simulate_single_risk_factor(model, simulation_dates, number_paths, number_of_risk_factors=1): I would assume that the input should include the number of risk drivers and (potentially their correlation)?
> Yes, absolutely (and btw: I forgot the correlation here). I have renamed the parameter number_of_risk_drivers. The main assumption I had to make in the interest of time (and this pops up later again) is to have at most one risk driver per risk factor. I hope this is not too much of a restriction for what you had in mind. We shall definitely put the multi-risk-driver situation back in once we can breath again. 

5. I think that simulate_single_risk_factor output should be a data frame, as it was for the model functions before (rows=paths, column=time). If multiple risk drivers, multiple outputs, i.e. RF, risk_driver_1, risk_driver_2,… 
> Okay, I will change that with the next iteration. 

6. I suggest to define the volatility as the vol of the log(S(t)/S(0)) process, since this is the one that is directly quoted and primarily used in constructing the paths. Also, correlations are defined at the level of the returns (either log or absolute). And the change in definition percolates in the testing functions as well.
> I completely agree. I thought I had done that, but probably I missed something. Maye we can talk about what is missing. 

7.  What about other HW functions? Notice also that the ones implemented are methods of the class. But we may want to use them also outside the class? 
> They go into a SimulatedHW1FCurve object that only stores the short rate and computes discount factors using those functions. 

8. The construction of the market data requires a logical step when the computer is told which model to use for which RF, since e.g. the same RF can have both HF1W and HF2W calibrations. Alternatively, you can load all calibrations for all models available but you need to add the name of the model in the dictionary key, e.g. ‘GBM_EUR_USD_FX_RATE_initial_value’.
> Yes. The approach is the short-circuited one of the final approach. 

9. create_risk_factor_portfolio, I would change the name to e.g. simulated_risk_factors_set 
> Well, they should contain the non-simulated risk factors as well, so the not simulated ones as well. It is a discovery step.

10. The class RiskFactor is a bit ambiguous. Since you take care of simulated RFs only but we will have also non simulated ones. I did not have a real solution for this either…We can discuss.
> This class has a simulated member that decides that. 

11. The MultiRiskFactorSimulation seems to mix up RFs and risk_drivers. For example: correlation_matrix.get_sub_correlation_matrix([rf.name for rf in risk_factors]) should be done at the level of the risk drivers?
> Yes, it should. But currently I made the assumption of 1 RD per RF. 

12. In your design the scenario object does not have the simulated paths as attribute (and similarly the RiskFactor). We can discuss this.
> That object will live in the CCR Session. 

13. The __str__(self) method for ScenarioGenerator should be abstract as well (if possible at all) or be a children class method?
> As above fot the RiskFactorEvolution

14. What about the pricing calibration for a given RF (that may differ from the one used for the dynamics)?
> Lives in the pricers (I am currently on that). 


Discussion 21/11/2022:

Actions:

1) Andre' to go on with code revision with deadline 5/12/2022 (as for plan A-B-C below). 
2) Andre' to write in the Note section the overall status of the code (what is ready and what is not) on 24/11/2022. 
3) Fabrizio to review the code before catch-up 28/11/2022.


Action plans:

A) Andre' to complete RF/Scenarios components and integrate them leaving the rest of the code in its present state.

B) Andre' to reduce the scope of A to only integrating the RFEevolution abstract class.

C) Rely on the original code base.


Notes:
- refactored the data folder. naming conventions, kept the csvs, rewrote the configuration, kept calibration data in one folder because that one should be ultimately deleted when calibration comes from models 


Discussion 21 Nov
- HW1F should simulate curves, how did you do that? FAn: HW1F r(t) allows to construct any discount factor you need at time t. Therefore I simply keep the short rate at the level of the scenario definition and construct the discount factor with the closed-form formula for the bond PtT at the point of valuing the trade. 
- correlation matrix making positive definite does not work yet FAn: there is already an algorithm to make the matrix semi-positive.
- debugging example 2 

Points FA 17/11/2022:
1. I think it is better to keep the calibration as a single dictionary, since models may be quite different and you want to access it in one go.
Completely agree, I will change that.

2. Related to the above you may want for the same model to access multiple calibrations (e.g. simulation and pricing) and it comes more handy if they are compacted in dictionaries.
I saw this in the code, but I am not sure I can imagine a usecase for it. Would you have an example for this? Having different drifts for simulation and pricing can make sense, but these are typically well-defined transformation from each other (real-world vs risk-neutral drifts). Do you have a more complex example? Or how would you create two different calibrations from the same data? 

3. In the new design, I do not see the concept of risk drivers (hardly relevant for GBM or BM but important for e.g. HW2F or the multi-factor RFE models implemented). This is something that I was using a lot at the point of generating the scenarios
That will come back when assembling the scenario class. This is indeed crucial there, completely agree.

4. I am not sure if you intend to have a RFE_model class based on RiskFactorEvolution or not. Either ways, there are a number of attributes that comes handy (such as asset class, type, currency…) and it is also very useful to store the simulated scenarios as attributes of the object.
No, I wasn't intenting to. The reason is the single purpose principle for classes. The RiskFactorEvolution and subclasses are responsible for creating paths, and the scenario class is responsible for generating scenarios. The existing RFE_model class did (in my view) mix both, so I broke that apart. About the additional attributes, completely agree, I was planning to put this into a dictionary in the scenario class, but maybe this can be stored at the level of RFE as well. What do you think?

5. Notice as well that we intend that at some point we may use RFE_model for very different kind of scenarios and models (such 10d historical scenarios for FRTB).
Cool. In my view these are different types of scenario generation logics => subclasses of a scenario generation base class. Would you have a list of such logics (forward simulation, historical 10d, anything else?). Is this related to the method = 'simulation' vs 'transformation'? What is the latter?



Questions AS 07/10/2022:
- what is the positions_keeping_system used for? This is the equivalent to INSIGHT at CS, i.e. the system that has both the counterparty view and the desk view. It is used for the portfolio construction: i) when one creates a portfolio a Netting Agreement ID should be provided; ii) Trades in the agreement can be identified via the positions_keeping_system file; iii) for every trade the file provides also the name of the feed file (the equivalent of the desk feed) where the trade attributes can be found.
- backtesting_data is in which file format? The current implementation can also load the data directly from NASDAQ but this was not working at BoE, so I dump it in a .CSV file.
- what is the function of the All_RFs_Mapping.csv? This is the file where ALL supported RFs are caracterised. This file tells if a RF is simulated or not and, if simulated, it provides the model to be used. The file provides other attributes of the RFs that are relevant in valuation (for example if a IR curve is a base curve, simulated by the model, or a spread curve, simply added to its base curve to generate the scenarios). 
- may I refactor the library? class structure, orchestrator, interfaces We can discuss this on Monday. All can be done but it depends on scale & timing.
- which licence to choose? No clue...

Discussion on October 17
- AI: first get the RFE in the class structure
- Milestone: the first notebook working
- AI: Scenario Class
