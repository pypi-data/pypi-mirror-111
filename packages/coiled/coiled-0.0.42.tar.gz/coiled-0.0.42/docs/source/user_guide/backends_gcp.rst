GCP Backend
===========

You can have Coiled launch computations on Google Cloud Platform (GCP). Your
computations will run inside Coiled's Google Cloud account, this makes it easy
for you to get started quickly, without needing to set up any additional
infrastructure.

.. figure:: images/backend-coiled-gcp-vm.png

.. note::

   GCP support is currently experimental with new features under active
   development.

.. tip::

    In addition to the usual cluster logs, our current GCP backend support also
    includes system-level logs. This provides rich insight into any potential
    issues while GCP support is still experimental.


Switching Coiled to run on GCP
--------------------------------

To use Coiled on GCP select "GCP" in the "Cloud Backend Options" section of the
Account page of your Coiled account.


Region
------

GCP support is currently only available in the ``us-east1`` region. If you have
data in a different region on Google Cloud, you may be charged transfer fees.


Backend options
---------------

Similar to the AWS backend, the GCP backend uses
`preemptible instances <https://cloud.google.com/compute/docs/instances/preemptible>`_
for the workers by default. Note that GCP automatically terminates these after 24 hours.


.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``spot``
     - Whether or not to use preemptible instances for cluster workers
     - ``True``

See :ref:`AWS Example <backend_options_example>` for backend options usage.


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned to you.
