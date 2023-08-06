==================
Running Pipeline
==================

Pipeline is run within the pipeline engine by calling the corresponding
method and specifying timestamps of start_date and end_date:

.. code-block:: python

    pipe_df = engine.run_pipeline(pipe, start_date, end_date)


The method returns the two-index (date-asset) dataframe with columns
corresponding to pipeline entries. 



