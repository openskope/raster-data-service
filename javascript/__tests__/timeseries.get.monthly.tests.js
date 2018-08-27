const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a timeseries GET request selects first pixel of each band in first year of monthly 5x5x60 data cube for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0001-01&end=0001-12&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Dataset id should match that in the request', async function() {
        expect(response.entity.datasetId).toBe('monthly_5x5x60_dataset');
    });

	it ('Variable name should match that in the request', async function() {
        expect(response.entity.variableName).toBe('int16_variable');
    });

	it ('Boundary geometry type should be point', async function() {
        expect(response.entity.boundaryGeometry.type).toBe('Point');
    });

    it ('Boundary geometry coordinates should be array with requested lat and longitude ', async function() {
        expect(response.entity.boundaryGeometry.coordinates).toEqual( [-123, 45] );
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0001-01" );
        expect(response.entity.end).toEqual( "0001-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each band for first 12 months', async function() {
        expect(response.entity.values).toEqual( [100,200,300,400,500,600,700,800,900,1000,1100,1200] );
    });
    
    it ('Csv should comprise dates and values for each band for first 12 months', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0001-01,100"			+ "\n" +
        		"0001-02,200"			+ "\n" +
        		"0001-03,300"			+ "\n" +
        		"0001-04,400"			+ "\n" +
        		"0001-05,500"			+ "\n" +
        		"0001-06,600"			+ "\n" +
        		"0001-07,700"			+ "\n" +
        		"0001-08,800"			+ "\n" +
        		"0001-09,900"			+ "\n" +
        		"0001-10,1000"			+ "\n" +
        		"0001-11,1100"			+ "\n" +
        		"0001-12,1200"			+ "\n"
		);
    });

});

describe("When a timeseries GET request selects first pixel of each band in first year of monthly 5x5x60 data cube for float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/float32_variable?longitude=-123.0&latitude=45.0&start=0001-01&end=0001-12&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Dataset id should match that in the request', async function() {
        expect(response.entity.datasetId).toBe('monthly_5x5x60_dataset');
    });

	it ('Variable name should match that in the request', async function() {
        expect(response.entity.variableName).toBe('float32_variable');
    });

	it ('Boundary geometry type should be point', async function() {
        expect(response.entity.boundaryGeometry.type).toBe('Point');
    });

    it ('Boundary geometry coordinates should be array with requested lat and longitude ', async function() {
        expect(response.entity.boundaryGeometry.coordinates).toEqual( [-123, 45] );
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0001-01" );
        expect(response.entity.end).toEqual( "0001-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each band for first 12 months', async function() {
        expect(response.entity.values).toEqual( [100,200,300,400,500,600,700,800,900,1000,1100,1200] );
    });
    
    it ('Csv should comprise dates and values for each band for first 12 months', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, float32_variable"	+ "\n" +
        		"0001-01,100"				+ "\n" +
        		"0001-02,200"				+ "\n" +
        		"0001-03,300"				+ "\n" +
        		"0001-04,400"				+ "\n" +
        		"0001-05,500"				+ "\n" +
        		"0001-06,600"				+ "\n" +
        		"0001-07,700"				+ "\n" +
        		"0001-08,800"				+ "\n" +
        		"0001-09,900"				+ "\n" +
        		"0001-10,1000"				+ "\n" +
        		"0001-11,1100"				+ "\n" +
        		"0001-12,1200"				+ "\n"
		);
    });

});


describe("When a timeseries GET request selects first pixel of each band in third year of monthly 5x5x60 data cube for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0003-01&end=0003-12&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0003-01" );
        expect(response.entity.end).toEqual( "0003-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each band for each month of third year', async function() {
        expect(response.entity.values).toEqual( [2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600] );
    });
    
    it ('Csv should comprise dates and values for each month in third year', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0003-01,2500"			+ "\n" +
        		"0003-02,2600"			+ "\n" +
        		"0003-03,2700"			+ "\n" +
        		"0003-04,2800"			+ "\n" +
        		"0003-05,2900"			+ "\n" +
        		"0003-06,3000"			+ "\n" +
        		"0003-07,3100"			+ "\n" +
        		"0003-08,3200"			+ "\n" +
        		"0003-09,3300"			+ "\n" +
        		"0003-10,3400"			+ "\n" +
        		"0003-11,3500"			+ "\n" +
        		"0003-12,3600"			+ "\n"
		);
    });
});

describe("When a timeseries GET request selects first pixel of each band in third year of monthly 5x5x60 data cube for float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/float32_variable?longitude=-123.0&latitude=45.0&start=0003-01&end=0003-12&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0003-01" );
        expect(response.entity.end).toEqual( "0003-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each band for each month of third year', async function() {
        expect(response.entity.values).toEqual( [2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600] );
    });
    
    it ('Csv should comprise dates and values for each month in third year', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, float32_variable"	+ "\n" +
        		"0003-01,2500"			+ "\n" +
        		"0003-02,2600"			+ "\n" +
        		"0003-03,2700"			+ "\n" +
        		"0003-04,2800"			+ "\n" +
        		"0003-05,2900"			+ "\n" +
        		"0003-06,3000"			+ "\n" +
        		"0003-07,3100"			+ "\n" +
        		"0003-08,3200"			+ "\n" +
        		"0003-09,3300"			+ "\n" +
        		"0003-10,3400"			+ "\n" +
        		"0003-11,3500"			+ "\n" +
        		"0003-12,3600"			+ "\n"
		);
    });
});

describe("When a timeseries GET request selects first pixel of each band in the 12 months starting at mid-year of year 4 of monthly 5x5x60 data cube for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0004-07&end=0005-06&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0004-07" );
        expect(response.entity.end).toEqual( "0005-06" );
    });
    
    it ('Values should be an array with one element for the first pixel for each of 12 months starting at mid-year of year 4', async function() {
        expect(response.entity.values).toEqual( [4300,4400,4500,4600,4700,4800,4900,5000,5100,5200,5300,5400] );
    });
    
    it ('Csv should comprise dates and values for 12 months starting at mid-year of year 4', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0004-07,4300"			+ "\n" +
        		"0004-08,4400"			+ "\n" +
        		"0004-09,4500"			+ "\n" +
        		"0004-10,4600"			+ "\n" +
        		"0004-11,4700"			+ "\n" +
        		"0004-12,4800"			+ "\n" +
        		"0005-01,4900"			+ "\n" +
        		"0005-02,5000"			+ "\n" +
        		"0005-03,5100"			+ "\n" +
        		"0005-04,5200"			+ "\n" +
        		"0005-05,5300"			+ "\n" +
        		"0005-06,5400"			+ "\n"
		);
    });
});

describe("When a values GET request selects first pixel of each band in year starting at mid-year of last year of monthly 5x5x60 data cube for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0005-07&end=0005-12&timeResolution=month&timeZero=0001-01'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0005-07" );
        expect(response.entity.end).toEqual( "0005-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each month starting at mid-year of last year', async function() {
        expect(response.entity.values).toEqual( [5500,5600,5700,5800,5900,6000] );
    });
    
    it ('Csv should comprise dates and values for each month starting at mid-year of last year of monthly 5x5x60 data cube', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0005-07,5500"			+ "\n" +
        		"0005-08,5600"			+ "\n" +
        		"0005-09,5700"			+ "\n" +
        		"0005-10,5800"			+ "\n" +
        		"0005-11,5900"			+ "\n" +
        		"0005-12,6000"			+ "\n"
		);
    });
});

describe("When a values GET request selects first pixel of each band in first year of monthly 5x5x60 data cube with an 18-month time zero offset for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0002-07&end=0002-12&timeResolution=month&timeZero=0002-07'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0002-07" );
        expect(response.entity.end).toEqual( "0002-12" );
    });
    
    it ('Values should be an array with one element for the first pixel of each of the first six months in the data set', async function() {
        expect(response.entity.values).toEqual( [100,200,300,400,500,600] );
    });
    
    it ('Csv should comprise dates and values for each of the first six months in the data set', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0002-07,100"			+ "\n" +
        		"0002-08,200"			+ "\n" +
        		"0002-09,300"			+ "\n" +
        		"0002-10,400"			+ "\n" +
        		"0002-11,500"			+ "\n" +
        		"0002-12,600"			+ "\n"
		);
    });
});

describe("When a values GET request selects first pixel of each band in year starting at mid-year of last year of monthly 5x5x60 data cube with an 18-month time zero offset for int16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/int16_variable?longitude=-123.0&latitude=45.0&start=0007-01&end=0007-06&timeResolution=month&timeZero=0002-07'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0007-01" );
        expect(response.entity.end).toEqual( "0007-06" );
    });
    
    it ('Values should be an array with one element for each of the last six months in the data sets', async function() {
        expect(response.entity.values).toEqual( [5500,5600,5700,5800,5900,6000] );
    });
    
    it ('Csv should comprise dates and values for each of the last six months in the data set', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, int16_variable"	+ "\n" +
        		"0007-01,5500"			+ "\n" +
        		"0007-02,5600"			+ "\n" +
        		"0007-03,5700"			+ "\n" +
        		"0007-04,5800"			+ "\n" +
        		"0007-05,5900"			+ "\n" +
        		"0007-06,6000"			+ "\n"
		);
    });
});


describe("When a values GET request selects pixels with NODATA in each band in year starting at mid-year of last year of monthly 5x5x60 data cube with an 18-month time zero offset for float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/monthly_5x5x60_dataset/float32_variable?longitude=-119.0&latitude=42.0&start=0007-01&end=0007-06&timeResolution=month&timeZero=0002-07'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "0007-01" );
        expect(response.entity.end).toEqual( "0007-06" );
    });
    
    it ('Values should be an array with one element for each of the last six months in the data sets', async function() {
        expect(response.entity.values).toEqual( [null, null, null, null, null, null] );
    });
    
    it ('Csv should comprise dates and values for each of the last six months in the data set', async function() {
        expect(response.entity.csv).toEqual( 
        		"month, float32_variable"	+ "\n" +
        		"0007-01,"					+ "\n" +
        		"0007-02,"					+ "\n" +
        		"0007-03,"					+ "\n" +
        		"0007-04,"					+ "\n" +
        		"0007-05,"					+ "\n" +
        		"0007-06,"					+ "\n"
		);
    });
});



