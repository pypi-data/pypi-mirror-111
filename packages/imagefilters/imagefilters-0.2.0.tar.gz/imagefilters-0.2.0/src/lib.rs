use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod submodule;
use submodule::*;

#[pyclass]
struct ExampleClass {
    #[pyo3(get, set)]
    value: i32,
}

#[pymethods]
impl ExampleClass {
    #[new]
    pub fn new(value: i32) -> Self {
        ExampleClass { value }
    }
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pymodule]
fn filters(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExampleClass>()?;
    m.add_wrapped(wrap_pymodule!(submodule))?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;

    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from filters.submodule import SubmoduleClass

    let sys = PyModule::import(py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    sys_modules.set_item("filters.submodule", m.getattr("submodule")?)?;

    Ok(())
}
