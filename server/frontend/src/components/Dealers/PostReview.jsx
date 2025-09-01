import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState(null);
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let params = useParams();
  let id = params.id;
  let dealer_url = root_url + `djangoapp/dealer/${id}`;
  let review_url = root_url + `djangoapp/add_review`;
  let carmodels_url = root_url + `djangoapp/get_cars`;

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if(name.includes("null")) {
      name = sessionStorage.getItem("username");
    }
    
    // FIXED: Proper validation without duplicates
    if (!model || review.trim() === "" || date.trim() === "" || year.trim() === "") {
      alert("All details are mandatory");
      return;
    }

    // FIXED: Better model splitting with validation
    let model_split = model.split(" ");
    if(model_split.length < 2) {
      alert("Please select a valid car make and model");
      return;
    }
    let make_chosen = model_split[0];
    let model_chosen = model_split.slice(1).join(" ");

    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });

    console.log("Submitting review:", jsoninput);

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const json = await res.json();
      if (json.status === 200) {
        window.location.href = window.location.origin + "/dealer/" + id;
      } else {
        alert("Error submitting review: " + (json.message || "Unknown error"));
      }
    } catch (error) {
      alert("Failed to submit review: " + error.message);
    }
  };

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    if(retobj.status === 200) {
      // FIXED: retobj.dealer is an object, not array
      setDealer(retobj.dealer);
    }
  };

  const get_cars = async () => {
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();
    if(retobj.status === 200) {
      // FIXED: Use retobj.cars (not CarModels)
      setCarmodels(retobj.cars || []);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  // FIXED: Add loading check for dealer
  if (!dealer) {
    return (
      <div>
        <Header/>
        <div style={{margin:"5%"}}>
          <h1 style={{color:"darkblue"}}>Loading dealer information...</h1>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header/>
      <div style={{margin:"5%"}}>
        <h1 style={{color:"darkblue"}}>{dealer.full_name}</h1>
        
        {/* FIXED: Added value prop for controlled component */}
        <textarea 
          id='review' 
          cols='50' 
          rows='7' 
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review here..."
        ></textarea>
        
        <div className='input_field'>
          Purchase Date 
          <input 
            type="date" 
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>
        
        <div className='input_field'>
          Car Make 
          <select 
            name="cars" 
            id="cars" 
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>Choose Car Make and Model</option>
            {/* FIXED: Use make/model properties from backend */}
            {carmodels.map((carmodel, index) => (
              <option 
                key={index} 
                value={carmodel.make + " " + carmodel.model}
              >
                {carmodel.make} {carmodel.model}
              </option>
            ))}
          </select>        
        </div>

        <div className='input_field'>
          Car Year 
          <input 
            type="number" 
            value={year}
            onChange={(e) => setYear(e.target.value)} 
            max={new Date().getFullYear()} 
            min={2015}
          />
        </div>

        <div>
          <button className='postreview' onClick={postreview}>Post Review</button>
        </div>
      </div>
    </div>
  )
}

export default PostReview;
