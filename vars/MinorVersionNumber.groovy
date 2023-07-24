def call(Map config = [:]) {
    def fullVersion = Version(config);
    def match = fullVersion =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/;
    return match[0][2];
}