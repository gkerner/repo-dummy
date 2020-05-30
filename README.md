##### Description
prometheus Gauge type metrics exporter template, written in python+flask+prometheus client

##### Develop Steps
1. Modify configs/config.yaml
2. Define metrics in core/custom_metric.py, just rewrite metrics_values function, and 
Initialize metric instance named m_instance
4. Generate supervisor configuration file
