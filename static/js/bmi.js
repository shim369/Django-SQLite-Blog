
let weightInput = document.getElementById('weight');
let heightInput = document.getElementById('height');

let bmiResult = document.getElementById('bmi-result');

let bmiTable = document.getElementById('bmi-table');

calculateBMI = (weight, height) => {
    return weight / (height * height);
};


updateBMITableView = (bmi) => {
    let st1 = document.getElementById('st1');
    let st2 = document.getElementById('st2');
    let st3 = document.getElementById('st3');
    let st4 = document.getElementById('st4');
    let st5 = document.getElementById('st5');
    let st6 = document.getElementById('st6');
    let st7 = document.getElementById('st7');
    let st8 = document.getElementById('st8');
    switch (true) {
        case bmi <= 15.99:
            st1.classList.add("p-article__bg-color");
            break;
        case bmi <= 16.99:
            st2.classList.add("p-article__bg-color");
            break;
        case bmi <= 18.49:
            st3.classList.add("p-article__bg-color");
            break;
        case bmi <= 24.99:
            st4.classList.add("p-article__bg-color");
            break;
        case bmi <= 29.99:
            st5.classList.add("p-article__bg-color");
            break;
        case bmi <= 34.99:
            st6.classList.add("p-article__bg-color");
            break;
        case bmi <= 39.99:
            st7.classList.add("p-article__bg-color");
            break;
        case bmi >= 40:
            st8.classList.add("p-article__bg-color");
            break;
    }

};

document.getElementById('calculate-bmi').addEventListener('click', () => {

    let weight = weightInput.value;
    let height = heightInput.value / 100;

    let bmi = calculateBMI(weight, height);

    bmiResult.innerHTML = bmi.toFixed(2);

    updateBMITableView(bmi);
});