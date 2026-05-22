    function SearchBox({query,setQuery}){
      
        function handleChange(event){
            setQuery(event.target.value)
        }

        return(
            <>
                <input value={query} onChange={handleChange}/>
            </>

        )
    }

export default SearchBox;

    