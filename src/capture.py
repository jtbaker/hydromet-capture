from prefect import flow
from prefect.schedules import Cron
from db.connection import get_db, attach_ducklake


@flow(name="capture_hydromet_snapshot", log_prints=True)
def load_data():
    print("Creating DuckDB connection")
    connection = get_db()
    print("Connecting to DuckLake")
    attach_ducklake(connection)

    print(
        "Creating ephemeral table from 'https://hydromet.lcra.org/api/GetDataForAllSites'"
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS hydromet_snapshot AS 
        SELECT 
            CAST(trim(siteNumber) as TEXT) siteNumber,
            CAST(dateTime as TIMESTAMP) dateTime,
            CAST(trim(zoomLevel) as INT) zoomLevel,
            CAST(trim(agency) as TEXT) agency,
            CAST(trim(siteName) as TEXT) siteName,
            CAST(trim(siteType) as TEXT) siteType,
            CAST(trim(latitude) as FLOAT) latitude, 
            CAST(trim(longitude) as FLOAT) longitude,
            CAST(trim(rainfallRecent) as FLOAT) rainfallRecent,
            CAST(trim(rainfall30Minute) as FLOAT) rainfall30Minute,
            CAST(trim(rainfall1Hour) as FLOAT) rainfall1Hour,
            CAST(trim(rainfall2Hours) as FLOAT) rainfall2Hours,
            CAST(trim(rainfall3Hours) as FLOAT) rainfall3Hours,
            CAST(trim(rainfall6Hours) as FLOAT) rainfall6Hours,
            CAST(trim(rainfall12Hours) as FLOAT) rainfall12Hours,
            CAST(trim(rainfallToday) as FLOAT) rainfallToday,
            CAST(trim(rainfall1Day) as FLOAT) rainfall1Day,
            CAST(trim(rainfall2Days) as FLOAT) rainfall2Days,
            CAST(trim(rainfall3Days) as FLOAT) rainfall3Days,
            CAST(trim(rainfall4Days) as FLOAT) rainfall4Days,
            CAST(trim(rainfall5Days) as FLOAT) rainfall5Days,
            CAST(trim(rainfall1Week) as FLOAT) rainfall1Week,
            CAST(trim(rainfall2Weeks) as FLOAT) rainfall2Weeks,
            CAST(trim(rainfall30Days) as FLOAT) rainfall30Days,
            CAST(trim(rainfallMonth) as FLOAT) rainfallMonth,
            CAST(trim(rainfallPrevMonth) as FLOAT) rainfallPrevMonth,
            CAST(trim(rainfallYear) as FLOAT) rainfallYear,
            CAST(trim(rainfallPrevYear) as FLOAT) rainfallPrevYear,
            CAST(trim(stage) as FLOAT) stage,
            CAST(trim(batteryVoltage) as FLOAT) batteryVoltage,
            CAST(trim(nwsid) as TEXT) nwsid,
            CAST(trim(flow) as FLOAT) flow,
            CAST(isStale as BOOLEAN) isStale,
            CAST(trim(temperature) as FLOAT) temperature,
            CAST(trim(minimumTemperature) as FLOAT) minimumTemperature,
            CAST(trim(maximumTemperature) as FLOAT) maximumTemperature,
            CAST(trim(relativeHumidity) as FLOAT) relativeHumidity,
            CAST(trim(bankfullStage) as FLOAT) bankfullStage,
            CAST(trim(floodStage) as FLOAT) floodStage,
            CAST(trim(waterTemperature) as FLOAT) waterTemperature,
            CAST(trim(head) as FLOAT) head,
            CAST(trim(tail) as FLOAT) tail,
            CAST(trim(isLCRA) as BOOLEAN) isLCRA,
            CAST(trim(isCOA) as BOOLEAN) isCOA
            FROM read_json_auto('https://hydromet.lcra.org/api/GetDataForAllSites');
        """
    )

    print("Initializing ducklake hydroshot snapshot if does not exist")

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS ducklake.hydromet_snapshot 
        AS 
        SELECT * FROM hydromet_snapshot WHERE FALSE
        """
    )

    print("Inserting rows to DuckLake table")

    connection.execute(
        "INSERT INTO ducklake.hydromet_snapshot SELECT * FROM hydromet_snapshot"
    )

    print("Job complete")


if __name__ == "__main__":
    load_data()
    # load_data.deploy(
    #     name="capture_hydromet_snapshot",
    #     work_pool_name="k8s-work-pool",
    #     build=False,
    #     image="jasonbaker/hydromet-capture:latest",
    #     job_variables={"image_pull_policy": "Always"},
    #     schedule=Cron("0 * * * *", timezone="UTC"),
    # )
