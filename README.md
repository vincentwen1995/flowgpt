# flowgpt
This is the repository for hosting Flowtrader's AI hackathon project .

## Pre-requisites

* Python 3.11
* Docker
* docker-compose

## Overall Strategy Structure
The overall strategy follows a three-tier structure:

1. Factor: The factors are generated manually or derived from research reports.
2. Factor Combination: The combination of factors is determined by the ChatGPT model.
3. Strategy: The strategy is determined by the ChatGPT model with input from human expertise.

## Software Components

### 1. Daemon
The daemon component runs in the background and performs the following tasks:

1. Collects market data, news, and social media feeds.
2. Crawls research reports and generates factors based on the collected data.

### 2. CLI (Command-Line Interface)
The CLI component is run on-demand and follows the following workflow:

1. Meta Configuration: Specify meta parameters (e.g., diversity) in the configuration file.
2. Signal Input: Provide a signal input to the software, specifying the backtesting time period.
3. Factor Combination: The ChatGPT model generates multiple sets of factors. The software performs backtesting using each set of factors and stores the results in a database.
4. Interaction with ChatGPT: The software interacts with the ChatGPT model, providing event information (market data, news, social media feeds, etc.), backtesting results, and other relevant data. The ChatGPT model then generates strategies based on the provided information.
5. Human Expertise: The software seeks human input and expertise to further refine the strategies.
6. Final Strategy Selection: Based on the software's selected strategy, the software can connect to a trading exchange for live trading (future implementation).

## Usage

To use this software, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies specified in the requirements.txt file.
3. Configure the meta parameters and other settings in the configuration file `portfolio_manager/config.yaml`.
4. Run the daemon component in the background to collect data and generate factors.
5. Use the CLI component `python cli.py inference-srategy --start-dt 2023-06-01 --end-dt 2023-06-02` to specify the backtesting time period and interact with the ChatGPT model for strategy generation.
6. Refine the strategies with human input and expertise.
7. Connect the software to a trading exchange for live trading (future implementation).

Please refer to the documentation for detailed instructions on setting up and running the software components.

## License

This software is licensed under the [Apache License 2.0](LICENSE). Feel free to use and modify it according to your needs.
