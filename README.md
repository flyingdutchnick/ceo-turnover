# Predicting CEO turnover

Inevitably, over the life of a company, CEOs are hired and replaced. Here are some headlines from the past three months: 

- "Tidjane Thiam is forced out of Credit Suisse after a spying fiasco."

- "A hard act to follow: Bob Iger leaves Disney."

- "Should Jamie Dimon, Wall Street’s most celebrated boss, call it a day?"

- "Giants including Salesforce, Apple and Microsoft may get new bosses in the next year or two"

A new HBO series called Succession dramatizes the CEO transition: confusion among shareholders about the leadership of the company, uncertainty for employees, heightened regulatory scrutiny, and risk of becoming a takeover target.  Not all CEO transitions are infused with drama like Succession, but the lack of certainty that pervades every episode of the show is far from unusual. 

What if a CEO transition could be predicted? If boards could predict turnover events and get ahead of events, they might be able to improve communications, they might be able to prevent a turnover from happening in the first, or they might be able to accelerate successor planning. 

Recent advances in AI and cloud computing have made it possible to do this type of analysis at low cost. This project seeks to explore how we can use off-the-shelf analytics tools like XGBoost along with publicly available data to predict a CEO turnover event before it happens. Specifically, we set out to predict the following question:

    For a CEO at a company in a given month, will they leave their job in the next 12 months? (TRUE or FALSE)

Below we describe how we did it: the data used, our methodology, the results of our model and some suggested next steps.

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

-------
### Methodology

-------
### Results

-------
### Next steps: confronting the dark side of AI

The possibilities offered by AI are exciting. Through online courses, cloud services and technical chat forums, models that could once only be built by PhDs in econometrics or computer science labs at top universities are now being applied by guys in a basement on an AWS server. Some call this the "democratization of AI".

But for the companies making decisions on the basis of AI, there are ethical issues involved. In the case of predicting CEO turnover, we used publicly available data, but if boards wanted, they could significantly enhance the power of a predictive model by using in-house company data as an input. They could mine board meeting minutes, the communications of a CEO and their deputies, or the the emails of all company staff. This raises ethical questions. Companies can stay a step ahead of mushrooming "AI dilemmas" by answering the following questions: 

- Is the company's use of AI completely compliant with current (and likely future) laws and regulations? 
- Can the company explain what it is doing with AI and how its use of AI is fair and aligned with stakeholder expectations?
- Do we understand potential biases of our models? If so, how do we ensure checks and balances? 
- Do people who are affected by AI have a voice in the development process and a way to ensure their voice is heard?

We don't expect all companies to have answers ready, but we think it's the responsibility of boards to proactively debate these issues, understand the implications of AI and ensure the company has standards in place for the fair use of AI. Given the rapid progress in AI and the high stakes involved, boards should start these discussions today. 
