# Predicting CEO turnover

Inevitably, over the life of a company, CEOs are hired and replaced. Here are some headlines from the past three months: 

- "Tidjane Thiam is forced out of Credit Suisse after a spying fiasco."

- "A hard act to follow: Bob Iger leaves Disney."

- "Should Jamie Dimon, Wall Street’s most celebrated boss, call it a day?"

- "Giants including Salesforce, Apple and Microsoft may get new bosses in the next year or two"

A new HBO series called Succession dramatizes the CEO transition: confusion among shareholders about the leadership of the company, uncertainty for employees, heightened regulatory scrutiny, and risk of becoming a takeover target.  Not all CEO transitions are infused with drama like Succession, but the lack of certainty that pervades every episode of the show is far from unusual. 

What if a CEO transition could be predicted? If boards could predict turnover events and get ahead of events, they might be able to pre-emptively issue a press relase to address the uncertainty in the market. Investors, on the other hand, might use predictive data about turnover events as a "factor" to optimize their investing strategy. 

Recent advances in AI and cloud computing have made it possible to do this type of analysis at low cost. This project used off-the-shelf analytics tools like XGBoost along with publicly available data to predict a CEO turnover event before it happens. Specifically, we set out to predict an answer to the following question:

    For a CEO at a company in a given month, will they leave their job in the next 12 months? (TRUE or FALSE)

Below we describe in more detail 1) data used, 2) methodology, 3) results and 4) suggested next steps.

-------

### 1. Data

Wharton Research Data Services (WRDS) was used in preparing this predictive model of CEO turnover. This service and the data available thereon constitute valuable intellectual property and trade secrets of WRDS and/or its third-party suppliers. Our dataset contains the following variables. 

**Director data:**

- Date of birth
- Company name
- Role title
- Role start date
- Role end date
- Gender

**Performance data:** 

- Company name, ticker
- Date (year, month)
- Closing price

-------
### 2.Methodology

-------
### 3. Results

-------
### 4. Next steps

A natural way to strengthen the model would be to use internal company data. Boards with access to company communications could significantly enhance the power of a predictive model that predicts the turnover of top management at their company by using in-house company data as an input. They could mine board meeting minutes, the communications of a CEO and their deputies, or the the emails of all company staff. 

To advance with this line of work, businesses also need to invest in the human expertise to leverage the benefits of the new technology while minimizing potential downside risks. 

The German multinational software company SAP has an AI ethics advisory panel, steering committee, along with set of guiding principles and detailed ethics code to govern the use of AI. Microsoft and Google have published "AI Principles", while the OpenAI research organization founded by Elon Musk has published a charter that guides the organnization in "acting in the best interests of humanity throughout its development."

In conclusion, any models used for talent management or predicting turnover should carefully calibrate the use of artificial intelligence using human intelligence. 
