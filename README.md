
How it works in short:
    Firstly you initialize query by creating SqlQuery instance. 
    After you register as many SqlSection instances as you like in SqlQuery.
    SqlSection do only job to process data and do not store it.
    SqlContainer store processed data.
    Each SqlSection keep SqlContainer in attribute self.container as a result.
