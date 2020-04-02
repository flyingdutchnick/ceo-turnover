# Predicting CEO turnover

Inevitably, over the life of a company, CEOs are hired and replaced. Here are some headlines from the past three months: 

- "Tidjane Thiam is forced out of Credit Suisse after a spying fiasco."

- "A hard act to follow: Bob Iger leaves Disney."

- "Should Jamie Dimon, Wall Street’s most celebrated boss, call it a day?"

- "Talk of succession atop Big Tech grows louder: giants including Salesforce, Apple and Microsoft may get new bosses in the next year or two"

A new HBO series called Succession dramatizes the events surrounding some CEO transitions: confusion among shareholders about the direction of the company, uncertainty for employees and a CEO's team, heightened regulatory scrutiny, and an increased risk of becoming a takeover target.  Not all CEO transitions have as a high a dose of drama as portrayed in Succession, but these events are far from unusual. Many a CEO transition has gone bad. 

What if a CEO transition or crisis could be predicted before it emerges? If boards could predict turnover events, they might be able to prevent minor problems from blowing into major crises, or they might be able to accelerate planning for a successor. Recent advances in AI and cloud computing have removed constraints and make it possible to do this type of analysis at low cost, while following widely-available recipes. 

This project seeks to explore how we can use off-the-shelf analytics tools like the powerful XGBoost model along with publicly available data to predict a CEO turnover event before it happens. Specifically, we want to predict the following question:

   **"Will a CEO leave his or her job in the next 12 months?**

Below we describe our data used, our methodology, the results of our model and some suggested next steps.

-------

### Data

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

### Methodology

### Results

### Next steps

The implications of AI are unimaginable. But once you get past the initial excitement raised by the potential AI, you are quicly confronted with serious ethical issues where rules don't exist. Should a board mine the email communications of a CEO and their top management team? Should a board monitor the private life of their CEO? Should "water cooler" talk be monitored and taken into account? How do we ensure checks and balances? We don't have the answers, but we think it's the responsibility of everyone to proactively debate these issues and make hard choices or risk AI deciding what's best for us.
