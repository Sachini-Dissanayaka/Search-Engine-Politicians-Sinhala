import React, { useState } from "react";
import { Input, Accordion, Dropdown, Icon } from "semantic-ui-react";

const genderOptions = [
  {
    key: "පිරිමි",
    text: "පුරුෂ",
    value: "පිරිමි",
  },
  {
    key: "ගැහැණු",
    text: "ස්ත්‍රී",
    value: "ගැහැණු",
  },
];

const partyOptions = [
  {
    key: "එක්සත් ජාතික පක්ෂය",
    text: "එක්සත් ජාතික පක්ෂය",
    value: "එක්සත් ජාතික පක්ෂය",
  },
  {
    key: "ශ්රී ලංකා නිදහස් පක්ෂය",
    text: "ශ්‍රී ලංකා නිදහස් පක්ෂය",
    value: "ශ්රී ලංකා නිදහස් පක්ෂය",
  },
  {
    key: "ශ්රී ලංකා පොඩුවජන පෙරමුණ",
    text: "ශ්‍රී ලංකා පොදුජන පෙරමුණ",
    value: "ශ්රී ලංකා පොඩුවජන පෙරමුණ",
  },
  {
    key: "සමගි ඩෑන් බාලවේවා",
    text: "සමගි ජන බලවේගය",
    value: "සමගි ඩෑන් බාලවේවා",
  },
  {
    key: "ශ්රී ලංකා දෙමළ රජය",
    text: "ශ්‍රී ලංකා දෙමළ සංධානය",
    value: "ශ්රී ලංකා දෙමළ රජය",
  },
  {
    key: "ස්වාධීන",
    text: "ස්වාධීන පක්ෂය",
    value: "ස්වාධීන",
  },
];

const positionOptions = [
  {
    key: "සභාපති",
    text: "ජනාධිපති",
    value: "සභාපති",
  },
  {
    key: "අගමැති",
    text: "අගමැති",
    value: "අගමැති",
  },
  {
    key: "විපක්ෂ නායක",
    text: "විපක්ෂ නායක",
    value: "විපක්ෂ නායක",
  },
  {
    key: "මුදල් ඇමති",
    text: "මුදල් ඇමති",
    value: "මුදල් ඇමති",
  },
  {
    key: "ආරක්ෂක ඇමති",
    text: "ආරක්ෂක ඇමති",
    value: "ආරක්ෂක ඇමති",
  },
  {
    key: "සෞඛ්ය අමාත්ය",
    text: "සෞඛ්‍ය ඇමති",
    value: "සෞඛ්ය අමාත්ය",
  },
  {
    key: "පාර්ලිමේන්තුවේ කථානායක",
    text: "කථානායක",
    value: "පාර්ලිමේන්තුවේ කථානායක",
  },
];

const Search = ({
  loading,
  onSearch,
  handlegenderchange,
  handlepartychange,
  handlepositionchange,
}) => {
  const [activeIndex, setActiveIndex] = useState(-1);
  const onKeyPress = (e) => {
    if (e.charCode === 13) onSearch(e.target.value);
  };

  const handleValueChange = (e, val) => {
    console.log(val.value);
  };

  const handleAccordionClick = (e, titleProps) => {
    const { index } = titleProps;
    setActiveIndex(activeIndex === index ? -1 : index);
  };

  return (
    <div style={{ margin: "1rem", width: "600px" }}>
      <Input
        icon="search"
        placeholder="Search"
        fluid
        loading={loading}
        onKeyPress={onKeyPress}
      />
      <Accordion>
        <Accordion.Title
          active={activeIndex === 0}
          index={0}
          onClick={handleAccordionClick}
        >
          <Icon name="dropdown" />
          Filters
        </Accordion.Title>
        <Accordion.Content active={activeIndex === 0}>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div style={{ margin: "1rem" }}>
              <div>Gender</div>
              <Dropdown
                placeholder="Select Gender"
                selection
                clearable
                options={genderOptions}
                onChange={handlegenderchange}
              />
            </div>
            <div style={{ margin: "1rem" }}>
              <div>Political Party</div>
              <Dropdown
                placeholder="Select Political party"
                selection
                clearable
                options={partyOptions}
                onChange={handlepartychange}
              />
            </div>
            <div style={{ margin: "1rem" }}>
              <div>Position</div>
              <Dropdown
                placeholder="Select Position"
                selection
                clearable
                options={positionOptions}
                onChange={handlepositionchange}
              />
            </div>
          </div>
        </Accordion.Content>
      </Accordion>
    </div>
  );
};

export default Search;
