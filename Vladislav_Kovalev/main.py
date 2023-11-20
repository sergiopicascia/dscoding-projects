import logging
import pandas as pd
from strategies.strategy_class import StrategyCalculation
from results_tools.construct_result.construct_result import construct_result
from utils import (
    dataHotelsPath,
    dataGuestsPath,
    dataPreferencesPath,
    firstStrategyPath,
    secondStrategyPath,
    thirdStrategyPath,
    fourthStrategyPath,
)


if __name__ == "__main__":
    """
    The program must calculate the allocation of customers at hotels,
    considering the number of available rooms, the fact that each customer
    occupies exactly one room, and that each stay lasts only one night.
    The price paid by the customer is the unit price of the room discounted
    by the fraction of the discount to which the customer is entitled.
    """
    # logging config
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    # read the data
    dataHotels = pd.read_excel(dataHotelsPath)
    dataGuests = pd.read_excel(dataGuestsPath)
    dataPreferences = pd.read_excel(dataPreferencesPath)

    calculationModule = StrategyCalculation()

    # random: customers are randomly distributed to the rooms until the seats or customers are exhausted;
    logging.warning("Start 1 strategy calculating")
    resultFrameFirstStrategy = calculationModule.first_strategy_main(
        dataHotels=dataHotels,
        dataGuests=dataGuests,
    )
    logging.warning("Calculating is completed")

    # customer preference: customers are served in order of reservation (the customer number indicates the order)
    # and are allocated to the hotel based on their preference, until the seats or customers are exhausted;
    logging.warning("Start 2 strategy calculating")
    resultFrameSecondStrategy = calculationModule.second_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )
    logging.warning("Calculating is completed")

    # price: the places in the hotel are distributed in order of price, starting with the cheapest hotel
    # and following in order of reservation and preference until the places or customers are exhausted;
    logging.warning("Start 3 strategy calculating")
    resultFrameThirdStrategy = calculationModule.third_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )
    logging.warning("Calculating is completed")

    # vailability: places in hotels are distributed in order of room availability, starting with
    # the most roomy hotel and subordinately in order of reservation and preference
    # until places or clients are exhausted.
    logging.warning("Start 4 strategy calculating")
    resultFrameFourthStrategy = calculationModule.fourth_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )
    logging.warning("Calculating is completed")

    logging.warning("Construct and save resulting files")
    for resultFrame, resultPath in zip(
        [
            resultFrameFirstStrategy,
            resultFrameSecondStrategy,
            resultFrameThirdStrategy,
            resultFrameFourthStrategy,
        ],
        [
            firstStrategyPath,
            secondStrategyPath,
            thirdStrategyPath,
            fourthStrategyPath,
        ],
    ):
        resultFrameSave = construct_result(
            dataHotels=dataHotels,
            dataGuests=dataGuests,
            resultFrame=resultFrame,
        )

        # Merge priority
        resultFrameSave = (
            resultFrameSave.merge(
                dataPreferences[["guest", "hotel", "priority"]],
                how="left",
                left_on=["GUEST", "HOTEL"],
                right_on=["guest", "hotel"],
            )
            .drop(columns=["guest", "hotel"])
            .drop_duplicates("GUEST", keep="first")
        )

        resultFrameSave = resultFrameSave.rename({"priority": "PRIORITY"}, axis=1)

        resultFrameSave.to_excel(
            resultPath,
            index=False,
        )
    logging.warning("Script completed")
