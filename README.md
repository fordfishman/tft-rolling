# TFT Rolling

## Description
[tft-rolling.com](http://tft-rolling.com) is a Dash-based web app hosted on GCP. It is designed to help TFT players understand how likely 
they are to hit units based on their level, how contested they are, how many copies of a unit they need, and how many units of the
same cost are taken out of the unit pool. 

## Features
- A control panel allowing you to click to select your desired unit and specify aspects of the games state:
  - Desired star level of unit
  - Your team's level
  - Number of unit copies you already own
  - Number of unit copies other players own
  - Number of units of same cost out of the shop pool
- An output panel showing the expected number of rolls to hit your unit, as well as some figures in panels:
  - The probability of hitting your unit by a certain number of rolls. This plot shows the joint cumulative distribution function (CDF)
    of *n* geometric random variables, where *n* is the number of unit copies you need. The joint probability mass function (PMF) is
    calculated as the convolution of *n* geometric PMFs.
  - The expected number of rolls of hitting as the number of unit copies other players own changes.
  - The expected number of rolls of hitting as the number of units of the same cost out of the shop pool changes. 

## Deploy locally

To run locally on your machine, please follow the following:

```bash
# Clone the repository
git clone https://github.com/fordfishman/tft-rolling.git

# Navigate to the project directory
cd tft-rolling

# Install dependencies
pip install -r requirements.txt

# Run app
python -m -src.app
```

## To-do
- The site is not currently mobile-friendly. The size and orientation of the panels should change according to screen size.
- Memory constraints are a hinderance right now when multiple users are using the page.
- Class test scripts currently need to be updated set-to-set. Try to find a better solution. 


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a pull request.

## License
This project is licensed under the [BSD 3-Clause License](LICENSE).
