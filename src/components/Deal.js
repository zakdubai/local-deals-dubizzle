export default function Deal(props){
    return(
        <div className='deal'>
            <div className='deal-picture'>
                {props.thumbnail ? <img src={props.thumbnail} /> : <p>No picture</p>}
            </div>
            <div className='deal-information'>
                <div className='deal-name'>
                    <a href={props.url ? props.url : 'undefined'}>{props.title}</a>
                </div>
                <div className='deal-category'>
                    {props.category}
                </div>
                <div className='deal-features'>
                    features
                </div>
                <div className='deal-price'>
                    {props.price}
                </div>
                <div className='deal-posteddate'>
                    {props.posted_date}
                </div>
            </div>
        </div>
    )
}