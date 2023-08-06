==============
skerrorlearner
==============

``skerrorlearner`` is an **Error Learning Package** for Machine Learning use cases. It is **available for both Regression and Classification problems under Supervised Machine Learning**. This helps build models that **learn the error of the current model** being built. This approach is taken towards **Machine Learning Model Performance Improvement**.

Download Stats
--------------

|PyPi Downloads| |PyPi Monthly Downloads| |PyPi Weekly Downloads|

Documentation
-------------

You can read the documentation `here`_.

License
-------

`Apache License 2.0`_

Installation
------------

**Using pip**

You can use pip to install skerrorlearner. Copy the below command and paste in Command Prompt to install skerrorlearner.

   ``pip install skerrorlearner``

To upgrade the package, copy the below command and paste in Command Prompt to upgrade skerrorlearner.

   ``pip install skerrorlearner --upgrade``

Usage
-----

As we highly believe in hands-on rather than reading documentations, we have got usage guides in the form of .ipynb notebooks. Below are the linked usage guides.

- `Regression Use Case`_
- `Classification Use Case`_

Further, if you fork the Skerrorlearner Use Case Demo directory, you'll be able to get the data on top of which skerrorlearner was tested. You'll also be able to get the .ipynb notebook to understand how the library works.

Once you have forked the library, we'd highly recommend you to read the dockstring of each method falling under skerrorlearner package to know what parameters are to be passed and what is the use of the method.

Support & Advantages
--------------------

The library supports below algorithms to build Error Models.

*Regression Use Case*

+----------------------+----------------+
|Scikit Learn          |Non-Scikit Learn|
+======================+================+
|Linear Regression     |XGBoost         |
+----------------------+----------------+
|Support Vector Machine|LightGBM        |
+----------------------+----------------+
|Decision Tree         |                |
+----------------------+----------------+
|Random Forest         |                |
+----------------------+----------------+
|K-Nearest Neighbors   |                |
+----------------------+----------------+
|AdaBoost              |                |
+----------------------+----------------+
|GradientBoost         |                |
+----------------------+----------------+

*Classification Use Case*

+----------------------+----------------+
|Scikit Learn          |Non-Scikit Learn|
+======================+================+
|Logistic Regression   |XGBoost         |
+----------------------+----------------+
|Support Vector Machine|LightGBM        |
+----------------------+----------------+
|Decision Tree         |CatBoost        |
+----------------------+----------------+
|Random Forest         |                |
+----------------------+----------------+
|K-Nearest Neighbors   |                |
+----------------------+----------------+
|AdaBoost              |                |
+----------------------+----------------+
|GradientBoost         |                |
+----------------------+----------------+
|GaussianNB            |                |
+----------------------+----------------+

*Advantages*

- Supports Hackathon Data Prediction
- Supports Production Live Data Prediction


.. |PyPi Downloads| image:: https://static.pepy.tech/personalized-badge/skerrorlearner?period=total&units=international_system&left_color=black&right_color=orange&left_text=Total%20Downloads
 :target: https://pepy.tech/project/skerrorlearner
.. |PyPi Monthly Downloads| image:: https://static.pepy.tech/personalized-badge/skerrorlearner?period=month&units=international_system&left_color=black&right_color=orange&left_text=Monthly%20Downloads
 :target: https://pepy.tech/project/skerrorlearner
.. |PyPi Weekly Downloads| image:: https://static.pepy.tech/personalized-badge/skerrorlearner?period=week&units=international_system&left_color=black&right_color=orange&left_text=Weekly%20Downloads
 :target: https://pepy.tech/project/skerrorlearner

.. _here: https://github.com/IndrashisDas/skerrorlearner
.. _Apache License 2.0: https://github.com/IndrashisDas/skerrorlearner/blob/main/LICENSE
.. _Regression Use Case: https://github.com/IndrashisDas/skerrorlearner/blob/main/Skerrorlearner%20Use%20Case%20Demo/Skerrorlearner%20-%20Regression%20Use%20Case%20Demo/Skerrorlearner%20-%20Regression%20Use%20Case%20Demo.ipynb
.. _Classification Use Case: https://github.com/IndrashisDas/skerrorlearner/blob/main/Skerrorlearner%20Use%20Case%20Demo/Skerrorlearner%20-%20Classification%20Use%20Case%20Demo/Skerrorlearner%20-%20Classification%20Use%20Case%20Demo.ipynb


