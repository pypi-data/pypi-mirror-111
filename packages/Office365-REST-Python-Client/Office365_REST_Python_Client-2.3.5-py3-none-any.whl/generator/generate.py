from generator import load_settings
from generator.builders.type_builder import TypeBuilder

from office365.runtime.odata.odata_v3_reader import ODataV3Reader
from office365.runtime.odata.odata_v4_reader import ODataV4Reader


def generate_files(model, options):
    """
    :type model: office365.runtime.odata.odata_model.ODataModel
    :type options: ConfigParser
    """
    for name in model.types:
        type_schema = model.types[name]
        builder = TypeBuilder(type_schema, options)
        builder.build()
        if builder.status == "created":
            builder.save()


def generate_sharepoint_model(settings):
    reader = ODataV3Reader(settings.get('sharepoint', 'metadataPath'))
    model = reader.generate_model()
    generate_files(model, settings)


def generate_graph_model(settings):
    reader = ODataV4Reader(settings.get('microsoftgraph', 'metadataPath'))
    model = reader.generate_model()
    generate_files(model, settings)


if __name__ == '__main__':
    generator_settings = load_settings()
    # generate_graph_model(settings)
    generate_sharepoint_model(generator_settings)
