# Predicting CEO turnover

Inevitably, over the life of a company, CEOs are hired and replaced. Here are some headlines from the past three months: 

- "Tidjane Thiam is forced out of Credit Suisse after a spying fiasco."

- "A hard act to follow: Bob Iger leaves Disney."

- "Should Jamie Dimon, Wall Street’s most celebrated boss, call it a day?"

- "Giants including Salesforce, Apple and Microsoft may get new bosses in the next year or two"

A new HBO series called Succession dramatizes the CEO transition: confusion among shareholders about who is in charge, uncertainty for employees, regulatory scrutiny, and a takeover battle.  Not every CEO transition is infused with drama like in the series Succession, but the lack of certainty that pervades the show is representative of many a CEO replacement. 

What if a CEO transition could be predicted before it happened? If an indicator showed a risk of a turnover event happening, a board could get ahead of events and pre-emptively issue a press release to address the (unfounded) uncertainty in the market. Investors, on the other hand, might use predictive data about turnover events as a "factor" to balance their asset allocation. 

Recent advances in AI and cloud computing make it possible to do this type of analysis at low cost. In this project, we use off-the-shelf analytics tools like XGBoost along with publicly available data to predict a CEO turnover event before it happens. Specifically, we set out to predict the following question:

    For a CEO at a company in a given month, will they leave their job in the next 12 months? (TRUE or FALSE)

This post describes 1) Data used, 2) Methodology, 3) Results and 4) Next steps.

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

A logical way to strengthen the model would be to incorporate internal company data. Boards with access to company communications could enhance the power of the predictive model by using in-house company data as an input. They could mine board meeting minutes, the communications of a CEO and their deputies, or the the emails of all company staff. Off-the-shelf algorithms like Word2Vec can convert this raw text data into usable data for machine learning.

To advance with this line of work, businesses also need to invest in the human expertise to leverage the benefits of the new technology while minimizing potential downside risks. 

The German multinational software company SAP has an AI ethics advisory panel, steering committee, along with set of guiding principles and detailed ethics code that govern the use of AI. Microsoft and Google have both published "AI Principles", while the OpenAI research organization founded by Elon Musk and Sam Altman has published a charter that guides the organization in "acting in the best interests of humanity throughout its development."

In conclusion, any models used for talent management or predicting turnover should carefully calibrate the use of artificial intelligence using human judgment.
