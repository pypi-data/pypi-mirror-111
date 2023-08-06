"""Performance tracker module for LUCEN.
Metrics of intereset (v1.0)

-- per trader
-- Total P/L per day
-- PL profile per day
-- Number win / day
-- Number loss /day
-- pl list (for stats and hist)


"""


import os, sys, time, random, logging


#local import


import inspect
from brahma.configCore import *
#config core
#sys.path.append('../')
#from configCore import *



#defunct I believe - feb 2021
#lcl_folder = os.environ['FITNESS_FOLDER_USR']
#sys.path.append(lcl_folder)

#edit feb
#lcl_folder_ = os.environ['FITNESS_FOLDER_USR_NEW']
# #sys.path.append(lcl_folder_)

# modulename = 'decisions'

# if modulename not in sys.modules:
#     print ('You have not imported the {} module'.format(modulename))
#uncomment  - feb2021 ->  not finding "TraderEvaluation"


#logger.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logging.warning("fskl")
#logger = logging.getLogger("__main__")
#---old
#CONFIGPATH = os.path.join(os.path.expanduser('~'), 'tradingalgorithm', 'code', 'lucen', 'code', '')
#---add config folder to project
#sys.path.insert(0,CONFIGPATH)
#from config import *
#from market_metrics import *
#from vis import *

#------------NOV 2020------------------------------------------

#---module version. May 2021

class RootDecisionConstraint(object):
    pass

class TradeDecisionConstraint(RootDecisionConstraint):
    pass

class RootDecision(object):
    """Decision involve an entry and exit. This is the decision entry. Stimuli initiate a decision. We then resolve that decision
    as part of a fitness function

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, decision_type="", decision_status=None):
        if decision_status != "":
            self.DecisionType = decision_type
            self.DecisionStatus = decision_status
        else:
            print ("Critical Error in Decision Root")
            print (decision_status)
            print (decision_type)
            exit()

    def __str__(self):
        return ("Root decision - Must overload")

class OldTradeDecision(RootDecision):
    """Derived from our parent decision entry class. This is the decision entry. This is a decision entry for a financial trade.
    Required are trade details:
    1. market
    2. price
    3. action
    4. time/date

    Arguments:
        RootDecisionEntry {[type]} -- [description]
    """

    def __init__(self, decision_data = None):
        RootDecision.__init__(self,decision_type="trade", decision_status=decision_data['status'])

        self.Market = decision_data['market']
        self.Price = decision_data['price']
        self.Time = decision_data['time']
        self.Date = decision_data['date']
        self.DecisionTypes = {-1:'SELL', 1:'BUY', 0:'IDLE'}
        self.Decision = self.DecisionTypes[decision_data['action']]

    def __str__(self):
        return ("Market: {0} ; Decision Type: {1} ; Price {3}; Date  {2}".format(self.Market, self.Decision, self.Date, self.Price))

class DecisionProfile(object):
    """Decision Profile holder. This can be extended for more
    complex decision making algorithms. Trade decisions will simply
    have entry and exit. Decision profile closed by adding decision with
    status 0. returns decision with profile 2 ( a measured decision )


    Arguments:
        object {[type]} -- [description]

    """
    def __init__(self, decision = None, profile_type = "trade", min_number_decisions = 2):
        self.Decision_id = "decision_profile" + str(random.randint(1,100000))
        self.DecisionList = []
        self.Type = profile_type
        self.Status = "Open"
        #mnin nunber decisions required for evqaluation..
        self.minNumberRequired = min_number_decisions
        if decision != None:
            self.DecisionList.append(decision)


    def force_close_decision(self):
        """Shut down this decision profile
        """
        self.Status = 'Closed'


    def add_decision(self, decision):
        #print ("ADDING DECIIONS")
        #self.DecisionList.append(decision)
        d_result = None
        if decision.DecisionStatus == 0:
            #shutting down profile
            self.Status = 'Closed'
            self.DecisionList.append(decision)
            #print ("adding closed")
            #d_result = self.evaluate_thinking()
            #self.DecisionList.append(d_result)

        if decision.DecisionStatus == 1:
            #add decision
            self.Status = 'Open'
            self.DecisionList.append(decision)
            #print ("adding open")
            #d_result = self.evaluate_thinking()
            #self.DecisionList.append(d_result)
            #check against constraints
            #if test fail, set closed and add result
            #decion to list

        return d_result


    #obsolete!!!
    def evaluate_thinking(self):
        """get the result data for this decision profile

        Returns:
            [type] -- [description]
        """
        decisionResult = None
        if self.Type == "trade":
            decisionResult = TradeDecisionResult()
            decisionResult.evaluate_result(decision_profile=self.DecisionList)
            return decisionResult

        else:
            return decisionResult

class RootResult(object):
    """Root Decision for performance storing. All decisions end with a result. This is the root class
    of the result

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, decision_type = ""):
        self.DecisionType = decision_type
        self.Success = None
        self.Fitness = 0

    def __str__(self):
        return ""

class OldTradeDecisionResult(RootResult):
    """Class to determine and store trade decision outcomes

    Arguments:
        RootDecisionResult {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    def __init__(self):
        RootResult.__init__(self,decision_type="trade")

    def evaluate_result(self, decision_profile = None):
        """Determine Fitness and any other required metrics

        Keyword Arguments:
            decision_profile {[type]} -- [description] (default: {None})
        """
        #self.PL = pl
        #self.EntryTime = time_entry
        #self.ExitTime = time_exit
        pass




    def __str__(self):
        pass

class DailyPerformance(object):
    """Performance dataPerformance is discretised into daily buckets.
    This is used by the evolution classes to rank and select and
    is therefore generic. Simply defines fitness values.
    Data more specific to the actual decision can be made
    using the decision profile data
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, date):
        """Initialise by passing date for which data is relevant

        Arguments:
            date {[type]} -- [description]
        """

        self.DecisionProfiles = []  #decision profiles
                                    #(includes specialised results for real deciison results)
        self.Decisions = []         #all decisions

    def add_decision(self, decision):
        """Add result to daily data.

        Keyword Arguments:
            date {str} -- [description] (default: {""})
            time_entry {str} -- [description] (default: {""})
            time_exit {str} -- [description] (default: {""})
            market {str} -- [description] (default: {""})
            pl {float} -- [description] (default: {0.0})
        """

        #append decisions - general list
        self.Decisions.append(decision)

        #add/create new decision profile
        numberProfiles = len(self.DecisionProfiles)
        if numberProfiles > 0:
            if self.DecisionProfiles[numberProfiles-1].Status == "Open":
                #add to existing profile
                self.DecisionProfiles[numberProfiles - 1].add_decision(decision)
                return

            #closed status after adding decision
            if self.DecisionProfiles[numberProfiles-1].Status == "Closed":

               #need new profile
               decisionProfile = DecisionProfile(decision)
               self.DecisionProfiles.append(decisionProfile)
               decisionProfile = None
               return

        else:
            decisionProfile = DecisionProfile(decision)
            self.DecisionProfiles.append(decisionProfile)
            decisionProfile = None



    def __str__(self):
        return ("Date: {0} ; Number Trades: {1} ; Number + {2} ; Number - {3} ; Total PL {4}".format(self.Date, self.NumberOfTrades, self.NumberPositive, self.NumberNegative, self.TotalPL))

class BotPerformance(object):
    """Individual bt performance recorder.

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self):

        self.PerformanceHolder = {}
        self.LastDecision = None



    def __str__(self):
        return_str = ""
        for date,value in self.PerformanceHolder.items():
            return_str += ((self.PerformanceHolder[date].__str__()))
            return_str += "\n"
        return return_str

    def getLastBotDecision(self):
        return self.LastDecision

    def add_decision(self, decision, epoch):
        """add individual decision result data. e.g. trade If the date doesn't already exist, add it

        Keyword Arguments:
            date {str} -- [description] (default: {""})
            time_entry {str} -- [description] (default: {""})
            time_exit {str} -- [description] (default: {""})
            market {str} -- [description] (default: {""})
            pl {float} -- [description] (default: {0.0})

        """
        self.LastDecision = decision
        if epoch in self.PerformanceHolder:
            self.PerformanceHolder[epoch].add_decision(decision)
        else:
            dailyPerformace = DailyPerformance(epoch)
            self.PerformanceHolder[epoch] = dailyPerformace
            self.PerformanceHolder[epoch].add_decision(decision)
    '''
    def summarize(self):
        self.TotalPL = 0
        self.NumberDays = 0
        self.NumberTrades = 0
        self.NumberPositive = 0
        self.NumberNegative = 0
        self.DailyPL = []
        for date, data in self.PerformanceHolder.items():
            self.TotalPL += data.TotalPL
            self.NumberDays += 1
            self.NumberTrades += data.NumberOfTrades
            self.NumberPositive += data.NumberPositive
            self.NumberNegative += data.NumberNegative
            self.DailyPL.append(data.TotalPL)
    '''

    def GetLastDecision(self):
        return self.LastDecision

    def showDailyDecisions(self):
        '''Output daily decision lists for trader.
        '''

        for date, dp in self.PerformanceHolder.items():
            for decisionP in dp.DecisionProfiles:
                for decision in decisionP.DecisionList:
                    print (decision)


        print ("***---***")
        for date, dp in self.PerformanceHolder.items():
            for decision in dp.Decisions:
                print (decision)

    def output_summary(self):
        return ("TotalPL: {0} # Trade: {1} # Up {2} # Down {3} \n".format(self.TotalPL, self.NumberTrades, self.NumberPositive, self.NumberNegative))

class EvaluateDecisions(object):
    '''Root class of evaluation. Fitness value only.

    Arguments:
        object {[type]} -- [description]


    '''
    def __init__(self, bot, botPerformance):
        self.fitnessValue = 0.0
        self.decisionSummary = {}
        #agent in optimisation process and making decisions
        self.bot = bot
        #bot/agent performance which holds decision profiles made  -> discretised by day or anyother
        #discretising factor. Always need multiple dynamic process -> not required though. e.g. one day can work
        #but not good practice
        self.botPerformance = botPerformance
        #Fitness recorder of each Decision Profile


    def evaluateFitness(self):
        self.fitnessValue = 0.0


    def printDecisionSummary(self):
        print ("Must override in custom evaluation logic")

    def getTradeDecisionsForRecording(self):
        return None

class OldTraderEvaluation(EvaluateDecisions):
    '''
    Bespoke evaluation class for intra day trade decisions. Determine P/L


    Arguments:
        EvaluateDecisions {[type]} -- [description]
    '''
    def __init__(self, bot, BotPerformance):
        EvaluateDecisions.__init__(self,bot=bot, botPerformance=BotPerformance)

    @staticmethod
    def getRunningEval(decision, entry, current, market):
        #print ("running pl")
        fitness = 0.0

        difference = (entry - current) / pointConversion[market]

        if decision == 1:
            fitness = -1 * round(difference,2)

        if decision == -1:
            fitness = round(difference,2)


        return fitness

    def evaluateFitness(self):


        if self.botPerformance == None:
            self.fitnessValue = 0
            if DECISION_ADDING_MEC:
                print ("CALC FITNESS: Fitness set to zero as no decisions made. %s" % self.bot.Name)
            return

        if FITNESS_DEBUG:
            print (self.bot.Name)

        #loop over all discrete applications of dynamic pressure (e.g. day) and evaluate fitness
        #for each event. BotPerformance -> DailyPerformance -> decision profiles
        #e.g number days
        numberEpisodes = len(self.botPerformance.PerformanceHolder)

        decisionRecorder = {}
        decisionNumber = 0
        fitness =  0
        number_episode = 0
        destroy = False
        for episodeTag, episode in self.botPerformance.PerformanceHolder.items():

            numberDP = len(episode.DecisionProfiles)
            if FITNESS_DEBUG:
                print (numberDP)
            for decision_profile in episode.DecisionProfiles:
                if FITNESS_DEBUG:
                    print ("decison prof")
                    print (decision_profile.Status)
                if decision_profile.Status == "Closed":
                    fitnessVal = self.getDecisionProfileFitness(decision_profile)
                    fitness += fitnessVal
                    decisionData = self.getTradeDecisionsForRecording(decision_profile, fitnessVal, self.bot.Direction)
                    decisionRecorder[decisionNumber] = decisionData
                    decisionNumber += 1
                    if decisionNumber > 100:
                        destroy = True
                        break

                if destroy == True:
                    break

        if FITNESS_DEBUG:
            print ("Decision Recorder:")
            print (decisionRecorder)

        #record fitness
        self.fitnessValue = fitness
        if destroy == True:
            self.fintnessValue = -1000

        self.decisionSummary = decisionRecorder

        #debug print
        #print ("{0} : {1} : {2}".format(self.bot.Name, self.fitnessValue, self.decisionSummary))


    def getDecisionProfileFitness(self, decisionProfile=None):
        if decisionProfile != None:

            difference = (decisionProfile.DecisionList[0].Price - decisionProfile.DecisionList[1].Price) / pointConversion[self.bot.Market]

            if self.bot.Direction == 1:
                fitness = -1 * round(difference,2)

            if self.bot.Direction == -1:
                fitness = round(difference,2)



            return fitness





    def getTradeDecisionsForRecording(self, decisionProfile=None, fitness=0, direction = 0):
        decisionData = {}

        if decisionProfile != None:
            #build decision def
            decisionData["entryPrice"] = decisionProfile.DecisionList[0].Price
            decisionData["exitPrice"] = decisionProfile.DecisionList[1].Price
            decisionData["date"] = decisionProfile.DecisionList[0].Date
            decisionData["entryTime"] = decisionProfile.DecisionList[0].Time
            decisionData["exitTime"] = decisionProfile.DecisionList[1].Time
            decisionData["entryDecision"] = decisionProfile.DecisionList[0].Decision
            decisionData["exitDecision"] = decisionProfile.DecisionList[1].Decision
            decisionData["direction"] = direction
            decisionData["fitness"] = fitness

        return decisionData

    def printDecisionSummary(self):
        for decisionNumber, summary in self.decisionSummary.items():
            print ("{0} , {1} , {2} , {3}".format(summary["entryPrice"],summary["exitPrice"], summary["direction"], summary["fitness"]))

class Performance(object):

    """
    Main Performance class. Record and store metrics for optimisation/simulation.

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self):
        """Initialise performance instance
        """
        
        import random
        self.performance_id = "performance" + str(random.randint(100,100000))
        from datetime import date
        curr_date = str(date.today())
        self.date_started = curr_date
        #this holds the botperformance->dailyperformance->decisionprofiles->decisions
        self.bots = {}
        #current state of bot
        self.decision_state = {}

        #evaluation of decisions...after all the decisions have been made, we must evaluate them
        #we must create the custom class for this run. e.g a trade evaluation class. All required metrics
        #are in root evaluation class.
        self.evaluation = {}


    def parallelJoinPerformances(self, performances = []):
        for perf in performances:
            self.bots.update(perf.bots)

        print ("Joined performances:")
        
    def getLastBotDecision(self,botID):
        return self.bots[botID].getLastBotDecision()


    def showBotDecisions(self):
        for bot, botperformance in self.bots.items():
            botperformance.showDailyDecisions()

    def add_trader(self, bot=None):
        """Add a trader to the performance tracker

        Keyword Arguments:
            bot {trader} -- New trader to add (default: {None})
        """
        if bot != None:
            botID = bot.Name
            botPerformance = BotPerformance()
            self.bots[botID] = botPerformance

    def UpdateDecisions(self):
        """Update against, for eg, decision contraints
        """

        pass

    def dna_transcribed(self, data):
        """
        DNA has been transcribed. This tells us whether the bot is 
        looking to open  or close a decision.

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        i_d = data['victim']
        if TRANSCRIPTION_DEBUG:
            print ("looking for decision status")
            print ("Victim ID: {0}".format(i_d))
        if i_d in self.decision_state:
            if TRANSCRIPTION_DEBUG:
                print ("looking for decision status")
                print ("Victim ID: {0} Found".format(i_d))
            decision_status = self.decision_state[i_d]
            if decision_status == 0:
                #currently idle
                return 0
            else:
                #in decision territory!
                return 1
        if TRANSCRIPTION_DEBUG:
            print ("Cant find ID in decision tracker. Must be a first decision.")
            print ("Victim ID: {0}".format(i_d))
        #no decisions made yet so return status 0 and make a new decision.
        return 0

    """
    VOID
    def decision_performance(self, data):
        i_d = data['victim']
        fit = 0.0
        if i_d in self.decision_state:
            current_price  = data['current']
            decision_status = self.decision_state[i_d]
            if decision_status == 1:

                lastDecision =  self.getLastBotDecision(i_d)
                decision = data['decision']
                entry = lastDecision.Price

                current = data['current']
                market = data['market']
                fit = TraderEvaluation.getRunningEval(decision, entry, current, market)

                return fit

        return fit
    """




    def update_decision_status(self, decision, bot_id):
        if bot_id in self.decision_state:
            self.decision_state[bot_id] = decision.DecisionStatus
        else:
            self.decision_state[bot_id] = decision.DecisionStatus

        if DECISION_STATE_DEBUG:
            for botId, state in self.decision_state.items():
                print("id: {0} state: {1}".format( botId, state) )



    def add_decision(self, decision=None, epoch="", botID=""):
        """Add decision. This can be any decision derived from root

        Keyword Arguments:
            decision {[type]} -- [description] (default: {None})
            date {str} -- [description] (default: {""})
            botID {str} -- [description] (default: {""})
        """

        self.update_decision_status(decision, botID)

        if decision != None:

            if botID in self.bots:
                
                self.bots[botID].add_decision(decision, epoch)


            else:
                #print ("adding bot")
                botPerformance = BotPerformance()
                self.bots[botID] = botPerformance
                self.bots[botID].add_decision(decision, epoch)
                if DECISION_ADDING_MEC:
                    print ("adding performance for %s" %(botID) )

        if decision == None:
            print ("Critical Error. Adding Decision.")
            exit()

    
    def evaluateBots(self, agents):

        '''Evaluate all bots in game.

        Arguments:
            agents {[type]} -- [description]
        '''


        # modulename = 'decisions'
        # #print (sys.path)
        # if modulename not in sys.modules:
        #     print('You have not imported the {} module'.format(modulename))
            

        # if not 'TraderEvaluation' in inspect.getmembers(modulename):
        #     print('You have not imported the {} class'.format('TraderEvaluation'))
            
        #s()['TraderEvaluation'])

            #build evaluation structure for all bots in species
        
        EvaluationClass = 'Evaluation'

        for name, agent in agents.items():
            
            if name in self.bots:

                #update general build Nov 2020
                evalClass = eval(EvaluationClass)
                self.evaluation[name] = evalClass(agent, self.bots[name])
                #self.evaluation[name] = TraderEvaluation(agent, self.bots[name])
                self.evaluation[name].evaluateFitness()
            else:
                if DECISION_ADDING_MEC:
                    print ("Bot didn't make any decisions in its lifetime. %s" % (name))
                #print ("no decisions made")
                evalClass = eval(EvaluationClass)
                self.evaluation[name] = evalClass(
                    agent, None)


        #else:
        #        if DECISION_ADDING_MEC:
        #            print ("Bot didn't make any decisions in its lifetime")
        #            self.evaluation[name] = TraderEvaluation(agent, self.bots[name])
        #            self.evaluation[name].fitnessValue = 0


        #evaluate
        #for botName, evaluationAlg in self.evaluation.items():
        #    evaluationAlg.evaluateFitness()
        #    if FITNESS_DEBUG:
        #        print ("***Fitness***")
        #        print (evaluationAlg.fitnessValue)


    def outputDecisionPerformanceSummary(self):
        '''
        Output to screen decision Summary -> decision data and associated fitness
        '''
        print ("ND: {}".format(len(self.evaluation)))
        for botName, evalAlg in self.evaluation.items():
            evalAlg.printDecisionSummary()


    def outputStructure(self, dataManager = None, gen = 0):
        '''Output structures
        '''





    def outputAndRecordEvalResults(self, dataManager = None, gen = 0, population = None):
        '''Output evaluation results.
        Save best trader and output data to track optimisation via the data manager
        Genration tag required
        '''
        fitness_struc = {}

        for botName, evalAlg in self.evaluation.items():
            
            #logger.info('%s being recorded', botName)
            fitness_struc[botName] = evalAlg.fitnessValue
            try:
                dataManager.recordBotDecisions(generation = gen, content = evalAlg.decisionSummary, botName = botName)
            except:
                print ("an error occured recording decision.")
                #logger.critical('An error occured recording decision.')



            #try:
            #    dataManager.saveBotDecisions(generation = gen, content = evalAlg.decisionSummary, botName = botName)
            #except:
            #    print ("an error occured saving decision.")

            #success = False
            #while (success == False):
            '''
            print ("fitness: sending structures")
            try:
                #print (population)
                structure = population[botName].printStr()
                #print (structure)
                #print ("---")
                dataManager.recordBotStructures(generation = gen, content = structure, botName = botName)
                print ("--- str sent")
                
            except:
                print ("an error occured recording structure.")
                #create structure image & save
            '''

            
            '''
            OP_OUTPUT_FOLDER = os.path.join(os.path.expanduser('~'), 'tradingalgorithm','code','lucen' , 'output')

            directoryPATH = os.path.join(OP_OUTPUT_FOLDER, str(dataManager.optimsationID))

            imgSavePath = os.path.join(directoryPATH, "tracker", "gen" , str(gen), "")
            '''

            '''
            imgBuilder = StructureImage(structure=structure, botName = botName, outpath = imgSavePath)
            #print (botName#)
            #print (imgSavePath)


            #build and save image
            imgBuilder.BuildImage()

            try:
                #upload image
                dataManager.recordBotImage(generation=gen, botName = botName)
            except:
                print ("An error occured recording .")
            '''


        import json

        fitness_json = json.dumps(fitness_struc)

        if dataManager != None:

            #success = False
            #while (success == False):
            try:
                dataManager.saveFitnessValues(generation = gen, content = fitness_json)
            except:
                print ("an error occured saving fitness values")
            try:
                dataManager.recordFitnessValues(generation = gen, content = fitness_json)
                #success = True
            except:
                print ("an error occured recording fitness values")
                #logger.critical('An error occured recording fitness values')


    def SummarizeBotPerformance(self):
        for ind, data in self.bots.items():
            data.summarize()

    def output_bot_summary(self):
        for ind, data in self.bots.items():
            print(data.output_summary())

    def output_all_data(self):
        print (f'Number of bots:  {len(self.bots)}')
        for ind, value in self.bots.items():
            print (ind)
            #print (self.bots[ind])



if 'FITNESS_DATA_FOLDER_USR' in os.environ:
    
    userFitnessFolder = os.environ['FITNESS_DATA_FOLDER_USR']
    #print (userGenesFolder)
    sys.path.insert(0,userFitnessFolder)
    from fdecisions import *

else:
    pass
    #print ('no user fitness material')
