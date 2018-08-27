const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a GET request selects from a float32 datafile a coordinate with all integral values", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/float32_variable?longitude=-123.0&latitude=45.0&start=0&end=4&csv=true&array=true'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The nodata value should be the one defined in the data file', async function() {
        expect(response.entity.nodata).toEqual('NaN');
	});

    it ('No nodata values should be found', async function() {
        expect(response.entity.containsNodata).toEqual(false);
	});
    
    it ('The values array should contain the 5 pixel values', async function() {
        expect(response.entity.values).toEqual( [100, 200, 300, 400, 500] );
    });

    it ('The lowerBounds array should contain the 5 pixel values minus the uncertainty in each', async function() {
        expect(response.entity.lowerBounds).toEqual( [90, 180, 270, 360, 450] );
    });

    it ('The upperBounds array should contain the 5 pixel values plus the uncertainty in each', async function() {
        expect(response.entity.upperBounds).toEqual( [110, 220, 330, 440, 550] );
    });

    it ('The data column in the csv should comprise the values and upper and lower bounds', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,100,90.0000,110.000"						+ "\n" +
        		"1,200,180.000,220.000"						+ "\n" +
        		"2,300,270.000,330.000"						+ "\n" +
        		"3,400,360.000,440.000"						+ "\n" +
        		"4,500,450.000,550.000"						+ "\n"
		);
    });
});

describe("When a GET request selects from a float32 datafile a coordinate with all non-integral values", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/float32_variable?longitude=-121.0&latitude=43.0&start=0&end=4&csv=true&array=true'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The nodata value should be the one defined in the data file', async function() {
        expect(response.entity.nodata).toEqual('NaN');
	});

    it ('No nodata values should be found', async function() {
        expect(response.entity.containsNodata).toEqual(false);
	});
    
    it ('The array should contain the 5 pixel values', async function() {
        expect(response.entity.values[0]).toBeCloseTo(122.2,3);
        expect(response.entity.values[1]).toBeCloseTo(222.2,3);
        expect(response.entity.values[2]).toBeCloseTo(322.2,3);
        expect(response.entity.values[3]).toBeCloseTo(422.2,3);
        expect(response.entity.values[4]).toBeCloseTo(522.2,3);
    });
    
    it ('The lowerBounds array should contain the 5 pixel values minus the uncertainty in each', async function() {
        expect(response.entity.lowerBounds[0]).toBeCloseTo(110.0,3);
        expect(response.entity.lowerBounds[1]).toBeCloseTo(200.0,3);
        expect(response.entity.lowerBounds[2]).toBeCloseTo(290.0,3);
        expect(response.entity.lowerBounds[3]).toBeCloseTo(380.0,3);
        expect(response.entity.lowerBounds[4]).toBeCloseTo(470.0,3);
    });

    it ('The upperBounds array should contain the 5 pixel values plus the uncertainty in each', async function() {
        expect(response.entity.upperBounds[0]).toBeCloseTo(134.4,3);
        expect(response.entity.upperBounds[1]).toBeCloseTo(244.4,3);
        expect(response.entity.upperBounds[2]).toBeCloseTo(354.4,3);
        expect(response.entity.upperBounds[3]).toBeCloseTo(464.4,3);
        expect(response.entity.upperBounds[4]).toBeCloseTo(574.4,3);
    });

    it ('The data column in the csv should comprise the values and upper and lower bounds', async function() {
        expect(response.entity.csv).toEqual(
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,122.200,110.000,134.400"					+ "\n" +
        		"1,222.200,200.000,244.400"					+ "\n" +
        		"2,322.200,290.000,354.400"					+ "\n" +
        		"3,422.200,380.000,464.400"					+ "\n" +
        		"4,522.200,470.000,574.400"					+ "\n"
		);
    });
});

describe("When a GET request selects from a float32 datafile a coordinate containing NODATA NaN values", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/float32_variable?longitude=-119.0&latitude=43.0&start=0&end=4&csv=true&array=true'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The nodata value should be the one defined in the data file', async function() {
        expect(response.entity.nodata).toEqual('NaN');
	});

    it ('A nodata value should be found', async function() {
        expect(response.entity.containsNodata).toEqual(true);
	});
    
    it ('The array should contain the 5 pixel values', async function() {
        expect(response.entity.values[0]).toBeCloseTo(124.4,3);
        expect(response.entity.values[1]).toBeCloseTo(224.4,3);
        expect(response.entity.values[2]).toBeNull()
        expect(response.entity.values[3]).toBeCloseTo(424.4,3);
        expect(response.entity.values[4]).toBeCloseTo(524.4,3);
    });
    
    it ('The lowerBounds array should contain the 5 pixel values minus the uncertainty in each', async function() {
        expect(response.entity.lowerBounds[0]).toBeCloseTo(112.0,3);
        expect(response.entity.lowerBounds[1]).toBeCloseTo(202.0,3);
        expect(response.entity.lowerBounds[2]).toBeNull();
        expect(response.entity.lowerBounds[3]).toBeCloseTo(382.0,3);
        expect(response.entity.lowerBounds[4]).toBeCloseTo(472.0,3);
    });

    it ('The upperBounds array should contain the 5 pixel values plus the uncertainty in each', async function() {
        expect(response.entity.upperBounds[0]).toBeCloseTo(136.8,3);
        expect(response.entity.upperBounds[1]).toBeCloseTo(246.8,3);
        expect(response.entity.upperBounds[2]).toBeNull();
        expect(response.entity.upperBounds[3]).toBeCloseTo(466.8,3);
        expect(response.entity.upperBounds[4]).toBeCloseTo(576.8,3);
    });

    it ('The data column in the csv should comprise the values and upper and lower bounds', async function() {
        expect(response.entity.csv).toEqual(
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,124.400,112.000,136.800"					+ "\n" +
        		"1,224.400,202.000,246.800"					+ "\n" +
        		"2,,,"										+ "\n" +
        		"3,424.400,382.000,466.800"					+ "\n" +
        		"4,524.400,472.000,576.800"					+ "\n"
		);
    });
});


