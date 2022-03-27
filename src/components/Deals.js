import Deal from './Deal'
import { useEffect, useState, useRef } from 'react';

export default function Deals(){
    // Variables used for the selection of the area
    const [areas,setAreas] = useState()
    const tempAreas = [];

    // URLs used by the Python script
    const API_URL_AREACODES = 'http://127.0.0.1:5000/areacodes/'
    const API_URL_AREADEALS = 'http://127.0.0.1:5000/localdeals/'

    // Current area selected by the user
    const [currentArea,setCurrentArea] = useState()

    // Variables used to display the local deals
    const fetchdeals = [];
    const [deals,setDeals] = useState();
    const i = useRef(0);

    // Variable used to track whether the areas have been downloaded, before fetching the list of deals
    const firstUpdate = useRef(true)


    // We first fetch the area codes
    useEffect(() => {
        fetch(API_URL_AREACODES)
        .then(res => res.json())
        .then(
            (result) => {                
                for (const [area,areacode] of Object.entries(result)){
                    tempAreas.push(<option key={i} value={areacode}>{area}</option>);
                    i.current = i.current + 1;
                }
                setAreas(tempAreas);
                firstUpdate.current = false;
            }
        )
    // eslint-disable-next-line react-hooks/exhaustive-deps
    },[])

    // We then fetch the deals corresponding to the area code
    // The hook will be called whenever the area code changes, i.e. the user selects a new area
    useEffect(() => {
        if(!firstUpdate.current){
            fetch(API_URL_AREADEALS + currentArea)
            .then(res => res.json())
            .then(
                (result)=> {
                    for(const key in result){
                        fetchdeals.push(
                            <Deal key={i}
                            title={result[key].title}
                            category={result[key].category}
                            posted_date={result[key].posted_date}
                            features={result[key].features}
                            thumbnail={result[key].thumbnail}
                            url={result[key].url}
                            price={result[key].price}/>
                        );
                        i.current = i.current + 1;
                    }
                    setDeals(fetchdeals);
                },
                (error)=> {
                    console.log(error)
            })
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    },[currentArea])

    // Function used to change the area
    function changeArea(e){
        setCurrentArea(e.target.value)
        setDeals()
    }

    const dropdownbox = <div><p>Select your area: </p><select onChange={changeArea}>{areas}</select></div>;
    const loadingdeals = <div><p>Loading deals...</p></div>
    const spinner = <div><p>Loading area codes...</p><div className="spinner"></div></div>

    return(
        <main>
            
            <div className='areas'>
                {areas ? dropdownbox : spinner}
            </div>

            <div className='deals'>
                {   currentArea && deals ?
                        deals : 
                        currentArea && loadingdeals
                        }
            </div>
        </main>
    )
}