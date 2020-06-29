# tapestry-server
The REST API server for the Tapestry Pooling Apps

This application is a REST API server to manage COVID PRC tests run using the Tapestry Project. Biologists/Experimenters from the labs running the tests to use the application to run PCR tests on large sample pools. The goal is to make the data collection and processing as automated and seamless as possible to scale and reduce human-error. 

The API's are consumed by the tapestry-webapp. 

## Highlevel Flow
- Biologists/Experimenters create a new test and specify the parameters of the test (machine type and configuration, Kit Type, Patient IDs etc) 
- Input data is processed and a matrix is generated, specifying which patient sample goes into which pools in the PCR machine. 
- After the test is performed they upload the experimental results back on the system and processed. 
- The final results (COVID-positive) patient IDs are returned.


