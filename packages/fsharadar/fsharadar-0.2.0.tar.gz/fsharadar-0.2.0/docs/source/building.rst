==================
Building Pipeline
==================

The Zipline pipeline framework is designed as an optimal set of base classes
(such as Pipeline Engine, Pipeline Loader, Factor, Pipeline) that can be
independently extended for producing an open collection of custom composite
applications. Then, building the pipeline represents a sequence of steps for
selecting and connecting together appropriate pipeline components. 


Pipeline Loaders
^^^^^^^^^^^^^^^^

The first step is associated with the selection of data bundles and
initialization of Pipeline Loaders. The *fsharadar*
module supports two bundles produced from Sharadar US Equity Prices (SEP)
and Daily Metrics of Core US Fundamental Data. According
to Zipline, each bundle can be independently accessed from the BundleData
instance that is retuned by the *load()* method provided by the corresponding
submodule, *sep* or *daily*, respectively. Subsequently, the BundleData instances
are used for initializing Pipeline Loaders. 

.. code-block:: python

    from fsharadar import sep
    from fsharadar import daily

    sep_bundle_data = sep.load()
    daily_bundle_data = daily.load()

    sep_pipe_loader = sep.PipelineLoader(sep_bundle_data)
    daily_pipe_loader = daily.PipelineLoader(daily_bundle_data)
    

Pipeline Engine
^^^^^^^^^^^^^^^

Th next step selects the appropriate PipelineEngine that propagates the Pipeline
collection of cross-sectional tasks (Factors or Classifiers) through the backtest
interval. The Zipline current version provides SimplePipelineEngine that computes
each task independently. The configuration of this engine requires the definition
of *get_loader* function and *asset_finder*. The *get_loader* function servers as
a dispatcher that returns the appropriate Pipeline Loader for retrieving raw data
of selected characteristic. 

.. code-block:: python

    from zipline.pipeline.engine import SimplePipelineEngine
    from zipline.pipeline.data import USEquityPricing

    def get_pipe_loader(column):
        if column in USEquityPricing.columns:
            return sep_pipe_loader
        if column in daily.Fundamentals.columns:
            return daily_pipe_loader
        raise ValueError("No PipelineLoader registered for column %s." % column)
    
    engine = SimplePipelineEngine(
        get_loader=get_pipe_loader,
        asset_finder=sep_bundle_data.asset_finder,
    )

Pipeline Universe
^^^^^^^^^^^^^^^^^

The pipeline universe defines a subset of stocks that meet a set of criteria. In Zipline, it can be implemented
by combining and nesting multiple Filters. Designed after the popular Quantopian version,  the *fsharadar* module provides the built-in TradableStocksUS universe that selects domestic common stocks with market cap bigger than $350 million, median daily dollar volume greater than or equal to 2.5 million over the trailing 200 days, and closing price higher than $5 per share.

.. code-block:: python

    from fsharadar.universe import TradableStocksUS
    universe = TradableStocksUS()

Pipeline Custom Factors
^^^^^^^^^^^^^^^^^^^^^^^

The pipeline task represents the computation of stock charecteristics within the trailing windows.
Some of the more popular computations (such as average, winsorize, zscore) are implemented
as Zipline built-in factors. This collection of common factors can be further
extended by specializing the CustomFactor class. The code snippet below shows
the implementation of the conventional momentum factor computed by ranking stocks according
to their prior behavior over the course of 11 months with a 1 month lag.

.. code-block:: python

    from zipline.pipeline.factors import CustomFactor
    from zipline.pipeline.data import USEquityPricing

    wl = 252
    class Momentum(CustomFactor):

        inputs = [USEquityPricing.close]
        window_length = wl
    
        def compute(self, today, assets, out, prices):
            out[:] = (prices[-21] - prices[-wl])/prices[-wl]


Pipeline
^^^^^^^^

Finally, application-related built-in and custom computations can be combined together
within a single Pipeline. The code snippet below shows a practical example used in Uncovering
Momentum studies
that explicitly explained the source of the momentum premium via high volatility growth stocks.
Specifically, the following pipeline includes two custom factors, Momentum (mom) and Realized
Volatility (rv), one built-in factor *cap* with market values for stocks, and a built-in classifier
*pb_quartile* computing quartiles based on stock price-to-book ratio. 

.. code-block:: python

    from zipline.pipeline import Pipeline
    from zipline.pipeline.factors import Latest

    def make_pipeline():
        pipe = Pipeline()
	pipe.add(Momentum(mask=universe), "mom")
        pipe.add(RealizedVolatility(mask=universe), "rv")	
        pipe.add(Latest([daily.Fundamentals.marketcap], mask=universe), 'cap')
	pipe.add(daily.Fundamentals.pb.latest.quartiles(mask=universe), "pb_quartile")

        pipe.set_screen(universe)
        return pipe

    pipe = make_pipeline()




