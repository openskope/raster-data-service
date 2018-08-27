const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a GET request selects a pixel with all nodata values and sets nodata parameter to ignore", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=42.0&start=0&end=4&csv=true&array=true&nodata=ignore'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Values should contain the nodata values', async function() {
        expect(response.entity.values).toEqual([65535,65535,65535,65535,65535]);
	});

    it ('The nodata values should be ignored', async function() {
        expect(response.entity.containsNodata).toEqual(false);
	});

    it ('Nodata should be null', async function() {
        expect(response.entity.nodata).toEqual(null);
	});

    it ('Csv should contain the nodata values', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,65535"					+ "\n" +
        		"1,65535"					+ "\n" +
        		"2,65535"					+ "\n" +
        		"3,65535"					+ "\n" +
    			"4,65535"					+ "\n"
		);
    });
});


describe("When a GET request selects a pixel with one nodata value and sets nodata parameter to ignore", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=43.0&start=0&end=4&csv=true&array=true&nodata=ignore'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('Values should contain the nodata value', async function() {
        expect(response.entity.values).toEqual([124,224,65535,424,524]);
	});
    
    it ('The nodata values should be ignored', async function() {
        expect(response.entity.containsNodata).toEqual(false);
	});

    it ('Nodata should be null', async function() {
        expect(response.entity.nodata).toEqual(null);
	});

    it ('Csv should contain the nodata value', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,124"						+ "\n" +
        		"1,224"						+ "\n" +
        		"2,65535"					+ "\n" +
        		"3,424"						+ "\n" +
    			"4,524"						+ "\n"
		);
    });
});

describe("When a GET request selects a pixel with one nodata value and sets nodata parameter to a value not present in the returned data", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=43.0&start=0&end=4&csv=true&array=true&nodata=1000'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('Values should contain the actual nodata value', async function() {
        expect(response.entity.values).toEqual([124,224,65535,424,524]);
	});
    
    it ('Response nodata should be the nodata value from the request', async function() {
        expect(response.entity.nodata).toEqual(1000);
	});

    it ('No nodata values should be reported', async function() {
        expect(response.entity.containsNodata).toEqual(false);
	});

    it ('Csv should contain the actual nodata value', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,124"						+ "\n" +
        		"1,224"						+ "\n" +
        		"2,65535"					+ "\n" +
        		"3,424"						+ "\n" +
    			"4,524"						+ "\n"
		);
    });
});

describe("When a GET request selects a pixel with no nodata value but sets nodata parameter to a value present in the returned data", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=44.0&start=0&end=4&csv=true&array=true&nodata=314'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('Values should contain the nodata value specified in request', async function() {
        expect(response.entity.values).toEqual([114,214,null,414,514]);
	});
    
    it ('Response nodata should be the nodata value from the request', async function() {
        expect(response.entity.nodata).toEqual(314);
	});

    it ('Detection of nodata values should be reported', async function() {
        expect(response.entity.containsNodata).toEqual(true);
	});

    it ('Csv should contain the nodata value specified in the request', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,114"						+ "\n" +
        		"1,214"						+ "\n" +
        		"2,"						+ "\n" +
        		"3,414"						+ "\n" +
    			"4,514"						+ "\n"
		);
    });
});


describe("When a GET request selects a pixel with one nodata value and accepts default behavior", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=43.0&start=0&end=4&csv=true&array=true'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('Values should contain the actual nodata value', async function() {
        expect(response.entity.values).toEqual([124,224,null,424,524]);
	});
    
    it ('Response nodata should be the nodata value detected in the data file metadata', async function() {
        expect(response.entity.nodata).toEqual(65535);
	});

    it ('Detection of a nodata value should be reported', async function() {
        expect(response.entity.containsNodata).toEqual(true);
	});

    it ('Csv should contain the actual nodata value', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,124"						+ "\n" +
        		"1,224"						+ "\n" +
        		"2,"						+ "\n" +
        		"3,424"						+ "\n" +
    			"4,524"						+ "\n"
		);
    });
});


describe("When a GET request selects a pixel with one nodata value and explicitly requests nodata detection from metadata", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-119.0&latitude=43.0&start=0&end=4&csv=true&array=true&nodata=detect'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('Values should contain the actual nodata value', async function() {
        expect(response.entity.values).toEqual([124,224,null,424,524]);
	});
    
    it ('Response nodata should be the nodata value detected in the data file metadata', async function() {
        expect(response.entity.nodata).toEqual(65535);
	});

    it ('Detection of a nodata value should be reported', async function() {
        expect(response.entity.containsNodata).toEqual(true);
	});

    it ('Csv should contain the actual nodata value', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,124"						+ "\n" +
        		"1,224"						+ "\n" +
        		"2,"						+ "\n" +
        		"3,424"						+ "\n" +
    			"4,524"						+ "\n"
		);
    });
})
