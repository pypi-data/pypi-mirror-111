### Calculator 

This is a python package hosted on PYPI and can be used to perform basic functions on calculator such as;
- ADDITION
- SUBTRACTION
- DIVISION
- MULTIPLICATION

It is an open source project with a public repository at https://github.com/linda-oranya/pypi_calculator.



### Installation

pypi_calculator requires python3 and can be installed via PYPI
``` shell
$ pip install ecalculator-pkg-linda-oranya
```
``` shell
$ pip install git+https://github.com/linda-oranya/pypi_calculator.git
```

### Usage
The calculator can be used for basic mathematical computation. The calculator has a memory that can reset itself to 0 and also stores previous values, except the memory is reset


Sample Code

``from calculator import Calculator``

cal = Calculator()
#### Addition

``cal.add(10)``

10

#### Subtraction
subtract

``cal.subtract(2)``

8

because the memory was not reset, 2 was subtracted from previous value 10

Division
For divide, zero division returns None and description

``cal.divide(2)``

4

``cal.divide(0)``

number cannot be zero => float division by zero
None

``cal.memory_val``

4

### Development
You can contribute to this project by cloning this repo and pushing to a branch for review and merging.

### Docker
pypi_calculator is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

## License

MIT

**It is a Free Software**